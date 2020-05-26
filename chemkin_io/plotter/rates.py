"""
Plot the rates from a CHEMKIN mechanism file
"""
import os
import subprocess
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


# Set plotting options
COLORS = ['k', 'b', 'r', 'g', 'm', 'y']
LINESTYLES = ['-', '--', '-.']
MARKERS = ['.', 'o', 's']

# Set various labels for plotting
FIG_TITLE = 'Comparison of Rate Data'
AXES_DCTS = [
    {'title': 'All rate constants'},
    {'title': 'Ratio of rate constants'}
]

FONT = {'size': 14}
matplotlib.rc('font', **FONT)


def build(ktp_dct, temps, dir_prefix='.', names=None):
    """ Generates plots of rate constants for all the reactions
        in two mechanisms.

        :param ktp_dct: k(T,P)s at all temps and pressures
        :type: dict[pressure: temps]
        :param temps: Temps used to calculate high- and low-k(T)s
        :type temps: numpy.ndarray
        :param dir_prefix: path where the plot directory will be built
        :type dir_prefix: str
        :param names: names of each reaction that serve as titles of their plot
        :type names: list(str)
    """

    # build new dct where we only have reactions with both mechs
    filt_ktp_dct = {}
    for reaction, ktps in ktp_dct.items():
        if list(ktps['mech1'].keys()) == list(ktps['mech2'].keys()):
            filt_ktp_dct[reaction] = ktps

    # Initialize file string to species and file names
    file_name_str = '{0:40s}{1}\n'.format('Name', 'Filename')

    # Set names to dict values if ther aren't anything
    if names is None:
        names = list(ktp_dct.keys())

    # Make the directory that holds the plots if it doesn't exist
    plot_dir = '{0}/rate_plots'.format(dir_prefix)
    if not os.path.exists(plot_dir):
        os.mkdir(plot_dir)

    # Plot the rate constants for each reaction
    reactions = list(filt_ktp_dct.keys())
    for i in range(0, len(reactions), 2):

        # Determine if plot will have two reactions in it, or one reaction
        if i+1 <= len(reactions)-1:
            nreactions = 2
        else:
            nreactions = 1

        # Create the figure object
        fig, axes = _build_figure(nreactions)

        # Set the axes object containing the plotted data for each reaction
        reaction_names = []
        for j in range(nreactions):
            # Determine the reaction dictionaries
            reaction = reactions[i+j]
            reaction_mech_ktp_dcts = [filt_ktp_dct[reaction]['mech1'],
                                      filt_ktp_dct[reaction]['mech2']]
            reaction_names.append(names[i+j])
            # Set variables needed for the plotting
            isbimol = _is_bimolecular(reaction)
            # Build the axes objects containing the plotted rate constants
            axes_col = axes[:, j] if nreactions == 2 else axes
            _build_axes(axes_col, reaction_mech_ktp_dcts, isbimol, temps)

        # Update figure title with the reaction(s) on the page
        _set_figure_title(fig, reaction_names)

        # Set the name of the plot
        file_name = 'r{0}'.format(str(i))
        file_name_str += '{0:40s}{1}\n'.format('reaction', file_name)

        # build and save the figure to a PDF
        fig_name = '{0}/{1}.pdf'.format(plot_dir, file_name)
        fig.savefig(fig_name, dpi=100)
        plt.close(fig)

    # # Collate all of the pdfs together
    # _collate_pdfs(plot_dir)

    # # Write file relating plot.pdf names to reaction names
    # with open(os.path.join(plot_dir, 'names.txt'), 'w') as name_file:
    #     name_file.write(file_name_str)


def _build_figure(nreactions):
    """ Initialize the size and format of the plot figure.

        :param nreactions: number of reactions on single page of figure
        :type nreactions: int
        :return: figure object for single page of plots
        :rtype: matplotlib.pyplot object
        :return: axes object for single page of plots
        :rtype: matplotlib.pyplot object
    """

    # Initialize plot objects
    if nreactions == 2:
        fig, axes = plt.subplots(
            nrows=2, ncols=2, figsize=(12, 8))
    else:
        grid = {'width_ratios': [0.5]}
        fig, axes = plt.subplots(
            nrows=2, ncols=1, figsize=(12, 8), gridspec_kw=grid)

    # Set various plot options
    fig.tight_layout()
    fig.subplots_adjust(left=0.075,
                        top=0.920, bottom=0.075,
                        wspace=0.2, hspace=0.175)

    return fig, axes


def _build_axes(ax_col, reaction_mech_dcts, isbimol, temps):
    """ plot the rates for various pressures
        certain checks are made throughout to deal with plotting
        only one reaction on a page

        :param ax_col: column of the axis
        :type ax_col: matplotlib.pyplot axis object
        :param isbimol: signal reaction is bimolecular
        :type isbimol: bool
        :param temps: Temperatures (K)
        :type temps: numpy.ndarray
        :return:
    """

    # Obtain a list of the pressures and sort from low to high pressure
    reaction_pressures_lst = [_get_sorted_pressures(list(reaction.keys()))
                              for reaction in reaction_mech_dcts]
    reaction_pressures_union = _get_union_pressures(reaction_pressures_lst)

    # Plot the data, setting formatting options for the axes
    _full_plot(ax_col[0], reaction_mech_dcts, reaction_pressures_lst, temps)
    _ratio_plot(ax_col[1], reaction_mech_dcts, reaction_pressures_union, temps)
    ax_col[0].set(**_set_axes_labels(AXES_DCTS[0], isbimol, bottom=False))
    ax_col[1].set(**_set_axes_labels(AXES_DCTS[1], isbimol, bottom=True))


def _full_plot(ax_obj, mech_ktp_dcts, mech_pressures, temps):
    """ Place data points corresponding to all of the rate constants 
        from the two mechanisms on a plot.

        :param ax_obj: axes onject to put points on
        :type ax_obj: matplotlib.pyplot object
        :param mech_ktp_dcts: rate constants for two mechanisms
        :type mech_ktp_dcts: list(dict[rxn: dict[pressure: rate constant]])
        :param mech_pressures: Pressures (atm)
        :type mech_pressures: list(float)
        :param temps: Temperatures (K)
        :type temps: list(float)
    """
    for i, ktp_dct in enumerate(mech_ktp_dcts):
        for j, pressure in enumerate(mech_pressures[i]):
            ax_obj.plot((1000.0/temps), np.log10(ktp_dct[pressure]),
                        color=COLORS[j], linestyle=LINESTYLES[i],
                        label='M'+str(i+1)+'-'+str(pressure))
    ax_obj.legend(loc='upper right')


def _ratio_plot(ax_obj, mech_ktp_dcts, pressures, temps):
    """ plot the ratio of rate constants from two mechanisms
    """
    [m1_ktp_dct, m2_ktp_dct] = mech_ktp_dcts
    for i, pressure in enumerate(pressures):
        m1_ktp = np.array(m1_ktp_dct[pressure])
        m2_ktp = np.array(m2_ktp_dct[pressure])
        ratios = m1_ktp / m2_ktp
        ax_obj.plot((1000.0/temps), ratios,
                    color=COLORS[i], linestyle=LINESTYLES[0],
                    label=pressure)
    ax_obj.legend(loc='upper left')


def _get_sorted_pressures(unsorted_pressures):
    """ get a sorted list of pressures for the reaction
    """
    if unsorted_pressures != ['high']:
        pressures = [pressure for pressure in unsorted_pressures
                     if pressure != 'high']
        pressures.sort()
    else:
        pressures = ['high']

    # Don't append 'high' to the dict to avoid plotting HighP rates
    # pressures.append('high')
    return pressures


def _get_union_pressures(pressures):
    """ get list of pressured where rates are defined for both mechanisms
    """
    [pr1, pr2] = pressures
    return list(set(pr1) & set(pr2))


def _is_bimolecular(reaction):
    """ Determines if a reaction is bimolecular
    """
    reactants = reaction[0]
    isbimol = bool(len(reactants) == 2)
    return isbimol


def _set_axes_labels(axes_dct, isbimol, bottom):
    """ alter the axes dictionary
    """
    if isbimol:
        units = 'cm3/s'
    else:
        units = '1/s'

    if bottom:
        axes_dct['xlabel'] = '1000/T (1000/K)'
        axes_dct['ylabel'] = 'k1/k2'
#        axes_dct['yscale'] = 'log'
    else:
        axes_dct['ylabel'] = 'log10 k({0})'.format(units)

    return axes_dct


def _set_figure_title(fig_obj, reactions_lst):
    """ Update the string for the figure title
    """
    reaction_str_lst = []
    for reaction in reactions_lst:
        side_strs = []
        for side in reaction:
            side_strs.append('+'.join(side))
        reaction_str_lst.append('='.join(side_strs))

    if len(reactions_lst) == 2:
        fig_title = '{0:^60s}{1:^60s}'.format(
            reaction_str_lst[0], reaction_str_lst[1])
    else:
        fig_title = '{0:^80s}'.format(
            reaction_str_lst[0])

    fig_obj.suptitle(fig_title)


def _collate_pdfs(plot_dir):
    """ collate all of the pdfs together
    """
    plots = [directory for directory in os.listdir(plot_dir)
             if 'pdf' in directory]
    plots.sort(key=lambda x: int(x.replace('r', '').replace('.pdf', '')))
    plots.append('all_rates.pdf')
    plots = [os.path.join(plot_dir, name) for name in plots]

    command = ['pdfunite'] + plots
    subprocess.call(command)
