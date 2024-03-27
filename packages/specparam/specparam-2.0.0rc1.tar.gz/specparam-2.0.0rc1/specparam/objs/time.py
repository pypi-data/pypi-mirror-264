"""Time model object and associated code for fitting the model to spectrograms."""

from functools import wraps

import numpy as np

from specparam.objs import SpectralModel, SpectralGroupModel
from specparam.plts.time import plot_time_model
from specparam.data.conversions import group_to_dict, group_to_dataframe, dict_to_df
from specparam.data.utils import get_results_by_ind
from specparam.core.utils import check_inds
from specparam.core.reports import save_time_report
from specparam.core.modutils import (copy_doc_func_to_method, docs_get_section,
                                     replace_docstring_sections)
from specparam.core.strings import gen_time_results_str

###################################################################################################
###################################################################################################

def transpose_arg1(func):
    """Decorator function to transpose the 1th argument input to a function."""

    @wraps(func)
    def decorated(*args, **kwargs):

        if len(args) >= 2:
            args = list(args)
            args[2] = args[2].T if isinstance(args[2], np.ndarray) else args[2]
        if 'spectrogram' in kwargs:
            kwargs['spectrogram'] = kwargs['spectrogram'].T

        return func(*args, **kwargs)

    return decorated


@replace_docstring_sections([docs_get_section(SpectralModel.__doc__, 'Parameters'),
                             docs_get_section(SpectralModel.__doc__, 'Notes')])
class SpectralTimeModel(SpectralGroupModel):
    """Model a spectrogram as a combination of aperiodic and periodic components.

    WARNING: frequency and power values inputs must be in linear space.

    Passing in logged frequencies and/or power spectra is not detected,
    and will silently produce incorrect results.

    Parameters
    ----------
    %copied in from SpectralModel object

    Attributes
    ----------
    freqs : 1d array
        Frequency values for the spectrogram.
    spectrogram : 2d array
        Power values for the spectrogram, as [n_freqs, n_time_windows].
        Power values are stored internally in log10 scale.
    freq_range : list of [float, float]
        Frequency range of the spectrogram, as [lowest_freq, highest_freq].
    freq_res : float
        Frequency resolution of the spectrogram.
    time_results : dict
        Results of the model fit across each time window.

    Notes
    -----
    %copied in from SpectralModel object
    - The time object inherits from the group model, which in turn inherits from the
      model object. As such it also has data attributes defined on the model object,
      as well as additional attributes that are added to the group object (see notes
      and attribute list in SpectralGroupModel).
    - Notably, while this object organizes the results into the `time_results`
      attribute, which may include sub-selecting peaks per band (depending on settings)
      the `group_results` attribute is also available, which maintains the full
      model results.
    """

    def __init__(self, *args, **kwargs):
        """Initialize object with desired settings."""

        SpectralGroupModel.__init__(self, *args, **kwargs)

        self._reset_time_results()


    def __getitem__(self, ind):
        """Allow for indexing into the object to select fit results for a specific time window."""

        return get_results_by_ind(self.time_results, ind)


    @property
    def n_peaks_(self):
        """How many peaks were fit for each model."""

        return [res.peak_params.shape[0] for res in self.group_results] \
            if self.has_model else None


    @property
    def n_time_windows(self):
        """How many time windows are included in the model object."""

        return self.spectrogram.shape[1] if self.has_data else 0


    def _reset_time_results(self):
        """Set, or reset, time results to be empty."""

        self.time_results = {}


    @property
    def spectrogram(self):
        """Data attribute view on the power spectra, transposed to spectrogram orientation."""

        return self.power_spectra.T


    @transpose_arg1
    def add_data(self, freqs, spectrogram, freq_range=None):
        """Add data (frequencies and spectrogram values) to the current object.

        Parameters
        ----------
        freqs : 1d array
            Frequency values for the spectrogram, in linear space.
        spectrogram : 2d array, shape=[n_freqs, n_time_windows]
            Matrix of power values, in linear space.
        freq_range : list of [float, float], optional
            Frequency range to restrict spectrogram to. If not provided, keeps the entire range.

        Notes
        -----
        If called on an object with existing data and/or results
        these will be cleared by this method call.
        """

        if np.any(self.freqs):
            self._reset_time_results()
        super().add_data(freqs, spectrogram, freq_range)


    def report(self, freqs=None, spectrogram=None, freq_range=None,
               peak_org=None, report_type='time', n_jobs=1, progress=None):
        """Fit a spectrogram and display a report, with a plot and printed results.

        Parameters
        ----------
        freqs : 1d array, optional
            Frequency values for the spectrogram, in linear space.
        spectrogram : 2d array, shape: [n_freqs, n_time_windows], optional
            Spectrogram of power spectrum values, in linear space.
        freq_range : list of [float, float], optional
            Frequency range to fit the model to. If not provided, fits the entire given range.
        peak_org : int or Bands
            How to organize peaks.
            If int, extracts the first n peaks.
            If Bands, extracts peaks based on band definitions.
        n_jobs : int, optional, default: 1
            Number of jobs to run in parallel.
            1 is no parallelization. -1 uses all available cores.
        progress : {None, 'tqdm', 'tqdm.notebook'}, optional
            Which kind of progress bar to use. If None, no progress bar is used.

        Notes
        -----
        Data is optional, if data has already been added to the object.
        """

        self.fit(freqs, spectrogram, freq_range, peak_org, n_jobs=n_jobs, progress=progress)
        self.plot(report_type)
        self.print_results(report_type)


    def fit(self, freqs=None, spectrogram=None, freq_range=None, peak_org=None,
            n_jobs=1, progress=None):
        """Fit a spectrogram.

        Parameters
        ----------
        freqs : 1d array, optional
            Frequency values for the spectrogram, in linear space.
        spectrogram : 2d array, shape: [n_freqs, n_time_windows], optional
            Spectrogram of power spectrum values, in linear space.
        freq_range : list of [float, float], optional
            Frequency range to fit the model to. If not provided, fits the entire given range.
        peak_org : int or Bands
            How to organize peaks.
            If int, extracts the first n peaks.
            If Bands, extracts peaks based on band definitions.
        n_jobs : int, optional, default: 1
            Number of jobs to run in parallel.
            1 is no parallelization. -1 uses all available cores.
        progress : {None, 'tqdm', 'tqdm.notebook'}, optional
            Which kind of progress bar to use. If None, no progress bar is used.

        Notes
        -----
        Data is optional, if data has already been added to the object.
        """

        super().fit(freqs, spectrogram, freq_range, n_jobs, progress)
        if peak_org is not False:
            self.convert_results(peak_org)


    def drop(self, inds):
        """Drop one or more model fit results from the object.

        Parameters
        ----------
        inds : int or array_like of int or array_like of bool
            Indices to drop model fit results for.

        Notes
        -----
        This method sets the model fits as null, and preserves the shape of the model fits.
        """

        super().drop(inds)
        for key in self.time_results.keys():
            self.time_results[key][inds] = np.nan


    def get_results(self):
        """Return the results run across a spectrogram."""

        return self.time_results


    def get_group(self, inds, output_type='time'):
        """Get a new model object with the specified sub-selection of model fits.

        Parameters
        ----------
        inds : array_like of int or array_like of bool
            Indices to extract from the object.
        output_type : {'time', 'group'}, optional
            Type of model object to extract:
                'time' : SpectralTimeObject
                'group' : SpectralGroupObject

        Returns
        -------
        output : SpectralTimeModel or SpectralGroupModel
            The requested selection of results data loaded into a new model object.
        """

        if output_type == 'time':

            # Initialize a new model object, with same settings as current object
            output = SpectralTimeModel(*self.get_settings(), verbose=self.verbose)
            output.add_meta_data(self.get_meta_data())

            if inds is not None:

                # Check and convert indices encoding to list of int
                inds = check_inds(inds)

                # Add data for specified power spectra, if available
                if self.has_data:
                    output.power_spectra = self.power_spectra[inds, :]

                # Add results for specified power spectra
                output.group_results = [self.group_results[ind] for ind in inds]
                output.time_results = get_results_by_ind(self.time_results, inds)

        if output_type == 'group':
            output = super().get_group(inds)

        return output


    def print_results(self, print_type='time', concise=False):
        """Print out SpectralTimeModel results.

        Parameters
        ----------
        print_type : {'time', 'group'}
            Which format to print results out in.
        concise : bool, optional, default: False
            Whether to print the report in a concise mode, or not.
        """

        if print_type == 'time':
            print(gen_time_results_str(self, concise))
        if print_type == 'group':
            super().print_results(concise)


    @copy_doc_func_to_method(plot_time_model)
    def plot(self, plot_type='time', save_fig=False, file_name=None, file_path=None, **plot_kwargs):

        if plot_type == 'time':
            plot_time_model(self, save_fig=save_fig, file_name=file_name,
                            file_path=file_path, **plot_kwargs)
        if plot_type == 'group':
            super().plot(save_fig=save_fig, file_name=file_name, file_path=file_path, **plot_kwargs)


    @copy_doc_func_to_method(save_time_report)
    def save_report(self, file_name, file_path=None, add_settings=True):

        save_time_report(self, file_name, file_path, add_settings)


    def load(self, file_name, file_path=None, peak_org=None):
        """Load time data from file.

        Parameters
        ----------
        file_name : str
            File to load data from.
        file_path : str, optional
            Path to directory to load from. If None, loads from current directory.
        peak_org : int or Bands
            How to organize peaks.
            If int, extracts the first n peaks.
            If Bands, extracts peaks based on band definitions.
        """

        # Clear results so as not to have possible prior results interfere
        self._reset_time_results()
        super().load(file_name, file_path=file_path)
        if peak_org is not False and self.group_results:
            self.convert_results(peak_org)


    def to_df(self, peak_org=None):
        """Convert and extract the model results as a pandas object.

        Parameters
        ----------
        peak_org : int or Bands, optional
            How to organize peaks.
            If int, extracts the first n peaks.
            If Bands, extracts peaks based on band definitions.
            If provided, re-extracts peak features; if not provided, converts from `time_results`.

        Returns
        -------
        pd.DataFrame
            Model results organized into a pandas object.
        """

        if peak_org is not None:
            df = group_to_dataframe(self.group_results, peak_org)
        else:
            df = dict_to_df(self.get_results())

        return df


    def convert_results(self, peak_org):
        """Convert the model results to be organized across time windows.

        Parameters
        ----------
        peak_org : int or Bands
            How to organize peaks.
            If int, extracts the first n peaks.
            If Bands, extracts peaks based on band definitions.
        """

        self.time_results = group_to_dict(self.group_results, peak_org)
