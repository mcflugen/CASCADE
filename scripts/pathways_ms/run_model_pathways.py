# run file for
#
# ~******* CASCADE ********~
#
# for the manuscript titled:
#
# "The Future of Developed Barrier Systems: Pathways Toward Uninhabitability, Drowning, and Rebound"
#
"""----------------------------------------------------
Copyright (C) 2022 Katherine Anarde
----------------------------------------------------"""

# please follow the instructions at https://github.com/UNC-CECL/CASCADE for installing CASCADE

import numpy as np
import os

from cascade.cascade import Cascade

from barrier3d.tools.input_files import (
    yearly_storms,
    gen_dune_height_start,
    gen_alongshore_variable_rmin_rmax,
    shift_storm_intensity,
)

# for laptop and desktop, use all but one core; on supercomputer, use all cores; KA Macbook has 15
# num_cores = multiprocessing.cpu_count() - 1

# # ###############################################################################
# # run functions
# # ###############################################################################


def RUN_4_CASCADE_noAST_Rave_SLR_pt004_NoHumans(
    nt,
    rmin,
    rmax,
    name,
    storm_file,
    elevation_file,
    dune_file,
):

    # ###############################################################################
    # 4 - CASCADE with only one B3D model and no human dynamics
    # ###############################################################################
    # Use the starting interior domain from the 10,000 yr runs for each dune growth rate and run for 1000 years
    # or until the barrier drowns. All other modules (brie and human dymnamics modules) turned off. Can also use this
    # run script for the 10,000 year runs.

    # --------- INITIALIZE ---------
    datadir = "./cascade/data/pathways_data/"
    cascade = Cascade(
        datadir,
        name,
        storm_file=storm_file,
        elevation_file=elevation_file,
        dune_file=dune_file,
        parameter_file="RUN4-CASCADE-parameters.yaml",
        wave_height=1,
        wave_period=7,  # s (lowered from 10 s to reduce k_sf)
        wave_asymmetry=0.8,  # fraction approaching from left
        wave_angle_high_fraction=0.2,  # fraction of waves approaching from higher than 45 degrees
        sea_level_rise_rate=0.004,  # m/yr
        sea_level_rise_constant=True,  # linear SLR
        background_erosion=0.0,
        alongshore_section_count=1,  # only one B3D domain
        time_step_count=nt,
        min_dune_growth_rate=rmin,
        max_dune_growth_rate=rmax,
        num_cores=1,
        roadway_management_module=False,  # no roadway management
        alongshore_transport_module=False,  # no brie coupling
        beach_nourishment_module=False,  # no beach nourishment
        community_economics_module=False,  # no community dynamics
    )

    # --------- LOOP ---------

    for time_step in range(nt - 1):
        # Print time step to screen (NOTE: time_index in each model is time_step+1)
        print("\r", "Time Step: ", time_step, end="")
        cascade.update()
        if cascade.b3d_break:
            break

    # --------- SAVE ---------
    save_directory = "Run_Output/"
    cascade.save(save_directory)
    os.chdir("..")

    return cascade


def RUN_6_CASCADE_noAST_Rave_SLR_pt004_Roadways(
    nt,
    rmin,
    rmax,
    name,
    storm_file,
    elevation_file,
    dune_file,
    road_ele=1.7,
    road_width=20,
    road_setback=20,
    dune_design_elevation=3.7,
    dune_minimum_elevation=2.2,
    percent_water_cells_sensitivity=None,
    background_erosion=0.0,
):

    # ###############################################################################
    # 6 - CASCADE with only one B3D model and roadway management
    # ###############################################################################
    # Use the starting interior domain from the 10,000 yr runs for each dune growth rate and run for 1000 years
    # or until the barrier drowns. All other modules (beach nourishment, community dyanmics) turned off.

    # --------- INITIALIZE ---------
    datadir = "./cascade/data/pathways_data/"
    cascade = Cascade(
        datadir,
        name,
        storm_file=storm_file,
        elevation_file=elevation_file,
        dune_file=dune_file,
        parameter_file="RUN6-CASCADE-parameters.yaml",
        wave_height=1,
        wave_period=7,
        wave_asymmetry=0.8,
        wave_angle_high_fraction=0.2,
        sea_level_rise_rate=0.004,
        sea_level_rise_constant=True,
        background_erosion=background_erosion,
        alongshore_section_count=1,
        time_step_count=nt,
        min_dune_growth_rate=rmin,
        max_dune_growth_rate=rmax,
        num_cores=1,
        roadway_management_module=True,
        alongshore_transport_module=False,  # no brie coupling
        beach_nourishment_module=False,  # no beach nourishment
        community_economics_module=False,  # no community dynamics
        road_ele=road_ele,
        road_width=road_width,
        road_setback=road_setback,
        dune_design_elevation=dune_design_elevation,
        dune_minimum_elevation=dune_minimum_elevation,
    )

    # for sensitivity testing
    if percent_water_cells_sensitivity is not None:
        cascade.roadways[
            0
        ].percent_water_cells_touching_road = percent_water_cells_sensitivity

    # --------- LOOP ---------

    for time_step in range(nt - 1):
        # Print time step to screen (NOTE: time_index in each model is time_step+1)
        print("\r", "Time Step: ", time_step, end="")
        cascade.update()
        if cascade.b3d_break:
            break

    # --------- SAVE ---------
    save_directory = "Run_Output/"
    cascade.save(save_directory)
    os.chdir("..")

    return cascade


def RUN_7_CASCADE_noAST_Rave_variableSLR_NoHumans(
    nt,
    rmin,
    rmax,
    name,
    storm_file,
    elevation_file,
    dune_file,
    sea_level_rise_rate,
    sea_level_constant,
):

    # ###############################################################################
    # 7 - same as RUN 4 but with variable rates of SLR (i.e., no AST, no human dynamics)
    # ###############################################################################

    # --------- INITIALIZE ---------
    datadir = "./cascade/data/pathways_data/"
    cascade = Cascade(
        datadir,
        name,
        storm_file=storm_file,
        elevation_file=elevation_file,
        dune_file=dune_file,
        parameter_file="RUN7-CASCADE-parameters.yaml",
        wave_height=1,
        wave_period=7,
        wave_asymmetry=0.8,
        wave_angle_high_fraction=0.2,
        sea_level_rise_rate=sea_level_rise_rate,
        sea_level_rise_constant=sea_level_constant,
        background_erosion=0.0,
        alongshore_section_count=1,
        time_step_count=nt,
        min_dune_growth_rate=rmin,
        max_dune_growth_rate=rmax,
        num_cores=1,
        roadway_management_module=False,  # no roadway dynamics
        alongshore_transport_module=False,  # no brie coupling
        beach_nourishment_module=False,  # no beach nourishment
        community_economics_module=False,  # no community dynamics
    )

    # --------- LOOP ---------

    for time_step in range(nt - 1):
        # Print time step to screen (NOTE: time_index in each model is time_step+1)
        print("\r", "Time Step: ", time_step, end="")
        cascade.update()
        if cascade.b3d_break:
            break

    # --------- SAVE ---------
    save_directory = "Run_Output/"
    cascade.save(save_directory)
    os.chdir("..")

    return cascade


def RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
    nt,
    rmin,
    rmax,
    name,
    dune_design_elevation,
    storm_file,
    elevation_file,
    dune_file,
    overwash_filter,
    overwash_to_dune,
    nourishment_volume,
    beach_width_threshold,
    background_erosion,
    rebuild_dune_threshold,
):

    # ###############################################################################
    # 8 - nourish beach, rebuild dunes, and remove overwash from barrier interior
    # ###############################################################################

    # --------- INITIALIZE ---------
    datadir = "./cascade/data/pathways_data/"
    cascade = Cascade(
        datadir,
        name,
        storm_file=storm_file,
        elevation_file=elevation_file,
        dune_file=dune_file,
        parameter_file="RUN8-CASCADE-parameters.yaml",
        wave_height=1,
        wave_period=7,
        wave_asymmetry=0.8,
        wave_angle_high_fraction=0.2,
        sea_level_rise_rate=0.004,
        sea_level_rise_constant=True,
        background_erosion=background_erosion,
        alongshore_section_count=1,
        time_step_count=nt,
        min_dune_growth_rate=rmin,
        max_dune_growth_rate=rmax,
        num_cores=1,
        roadway_management_module=False,  # no roadway management
        alongshore_transport_module=False,  # no brie coupling
        beach_nourishment_module=True,
        community_economics_module=False,  # no community dynamics
        dune_design_elevation=dune_design_elevation,
        nourishment_interval=None,  # yrs
        nourishment_volume=nourishment_volume,  # m^3/m
        overwash_filter=overwash_filter,  # % overwash filtered by development
        overwash_to_dune=overwash_to_dune,  # % overwash bulldozed back to dune
    )

    # --------- LOOP ---------

    iB3D = 0  # we only have one Barrier3D domain here

    # after each year, check the beach width and dune elevation and decide if you want to nourish or rebuild the dune
    # next year with nourish_now parameter
    dune_rebuild_threshold = rebuild_dune_threshold + (
        cascade.barrier3d[iB3D].BermEl * 10
    )  # if rebuild_dune_threshold=0.3, this is the same threshold for abs. min elevation as in RoadwayManager (m MHW)

    for time_step in range(nt - 1):

        # Print time step to screen (NOTE: time_index in each model is time_step+1)
        print("\r", "Time Step: ", time_step, end="")
        cascade.update()
        if cascade.b3d_break:
            break

        # stop managing if the barrier becomes too narrow to sustain a community
        if cascade.community_break[iB3D]:
            pass
        else:
            t = cascade.barrier3d[iB3D].time_index

            if cascade.nourishments[iB3D].beach_width[t - 1] < beach_width_threshold:
                cascade.nourish_now[iB3D] = 1

            DuneDomainCrest = (
                cascade.barrier3d[iB3D].DuneDomain[t - 1, :, :].max(axis=1)
            )  # Maximum height of each row in dune domain [dam]
            # DuneRestart = cascade.barrier3d[iB3D].DuneRestart
            # DuneDomainCrest[DuneDomainCrest < DuneRestart] = DuneRestart
            DuneCrestMin = (
                np.min(DuneDomainCrest) + cascade.barrier3d[iB3D].BermEl
            ) * 10  # m MHW

            if DuneCrestMin < dune_rebuild_threshold:
                cascade.rebuild_dune_now[iB3D] = 1

    # --------- SAVE ---------
    save_directory = "Run_Output/"
    cascade.save(save_directory)
    os.chdir("..")

    return cascade


def RUN_9_CASCADE_Rave_SLR_pt004_AlongshoreVariableManagement(
    nt,
    name,
    storm_file,
    alongshore_section_count,
    num_cores,
    beach_width_threshold,  # not a parameter in cascade, for triggering: must be list
    rmin,  # the remaining variables are arrays
    rmax,
    elevation_file,
    dune_file,
    dune_design_elevation,
    dune_minimum_elevation,
    road_ele,
    road_width,
    road_setback,
    overwash_filter,
    overwash_to_dune,
    nourishment_volume,
    background_erosion,
    rebuild_dune_threshold,
    roadway_management_on,
    beach_dune_manager_on,
    sea_level_rise_rate=0.004,  # not an array
    sea_level_constant=True,  # not an array
    trigger_dune_knockdown=False,
    group_roadway_abandonment=None,
):

    # ###############################################################################
    # 9 - connect cascade domains (human management) with AST
    # ###############################################################################

    # --------- INITIALIZE ---------
    datadir = "./cascade/data/pathways_data/"
    cascade = Cascade(
        datadir,
        name,
        storm_file=storm_file,
        elevation_file=elevation_file,
        dune_file=dune_file,
        parameter_file="RUN9-CASCADE-parameters.yaml",
        wave_height=1,
        wave_period=7,
        wave_asymmetry=0.8,
        wave_angle_high_fraction=0.2,
        sea_level_rise_rate=sea_level_rise_rate,
        sea_level_rise_constant=sea_level_constant,
        background_erosion=background_erosion,
        alongshore_section_count=alongshore_section_count,
        time_step_count=nt,
        min_dune_growth_rate=rmin,
        max_dune_growth_rate=rmax,
        num_cores=num_cores,
        roadway_management_module=roadway_management_on,
        alongshore_transport_module=True,  # couple brie
        beach_nourishment_module=beach_dune_manager_on,
        community_economics_module=False,  # no community dynamics
        road_ele=road_ele,
        road_width=road_width,
        road_setback=road_setback,
        dune_design_elevation=dune_design_elevation,
        dune_minimum_elevation=dune_minimum_elevation,
        trigger_dune_knockdown=trigger_dune_knockdown,
        group_roadway_abandonment=group_roadway_abandonment,
        nourishment_interval=None,  # yrs
        nourishment_volume=nourishment_volume,  # m^3/m
        overwash_filter=overwash_filter,  # % overwash removed
        overwash_to_dune=overwash_to_dune,
    )

    # --------- LOOP ---------

    # after each year, check the beach width and dune elevation and decide if you want to nourish or rebuild the dune
    # next year with nourish_now parameter; just use first B3D domain, since all berm elevations are equivalent
    dune_rebuild_threshold = rebuild_dune_threshold + (
        cascade.barrier3d[0].BermEl * 10
    )  # if rebuild_dune_threshold=0.3, this is the same threshold for abs. min elevation as in RoadwayManager (m MHW)

    for time_step in range(nt - 1):

        # Print time step to screen (NOTE: time_index in each model is time_step+1)
        print("\r", "Time Step: ", time_step, end="")
        cascade.update()
        if cascade.b3d_break:
            break

        t = cascade.barrier3d[0].time_index
        tmp_rebuild_dune = np.zeros(alongshore_section_count)
        tmp_nourish_now = np.zeros(alongshore_section_count)

        for iB3D in range(alongshore_section_count):
            # don't do any beach/dune management activities if the barrier has become too narrow to sustain a community
            if cascade.community_break[iB3D]:
                pass
            # and only manage beach/dune if it is turned on
            elif beach_dune_manager_on[iB3D]:

                if (
                    cascade.nourishments[iB3D].beach_width[t - 1]
                    < beach_width_threshold[iB3D]
                ):
                    # cascade.nourish_now[iB3D] = 1
                    tmp_nourish_now[iB3D] = 1

                DuneDomainCrest = (
                    cascade.barrier3d[iB3D].DuneDomain[t - 1, :, :].max(axis=1)
                )  # Maximum height of each row in dune domain [dam]
                DuneCrestMin = (
                    np.min(DuneDomainCrest) + cascade.barrier3d[iB3D].BermEl
                ) * 10  # m MHW

                if DuneCrestMin < dune_rebuild_threshold:
                    # cascade.rebuild_dune_now[iB3D] = 1
                    tmp_rebuild_dune[iB3D] = 1

        # only nourish or rebuild dune if all segments fall below threshold (more realistic)
        if np.all(tmp_nourish_now[beach_dune_manager_on]) == 1:
            cascade.nourish_now = tmp_nourish_now
        if np.all(tmp_rebuild_dune[beach_dune_manager_on]) == 1:
            cascade.rebuild_dune_now = tmp_rebuild_dune

    # --------- SAVE ---------
    save_directory = "Run_Output/"
    cascade.save(save_directory)
    os.chdir("..")

    return cascade

# # ###############################################################################
# # record of runs
# # ###############################################################################

# record of B3D time series initial conditions (storms, dune growth rates, growth parameters) -------------------
def time_series():

    datadir = "./cascade/data/pathways_data/"

    StormSeries_NormDist_10kyrs_01 = yearly_storms(
        datadir=datadir,
        storm_list_name="StormList_20k_VCR_Berm1pt9m_Slope0pt04.csv",  # this is == "cascade_default_storm_list.csv"
        mean_yearly_storms=8.3,
        SD_yearly_storms=5.9,
        MHW=0.46,  # m NAVD88
        StormStart=2,
        BermEl=1.9,  # m NAVD88, just used for plotting
        model_years=10000,
        bPlot=True,
        bSave=True,
        output_filename="StormSeries_10kyrs_VCR_Berm1pt9m_Slope0pt04_01",
    )

    StormSeries_NormDist_10kyrs_02 = yearly_storms(
        datadir=datadir,
        storm_list_name="StormList_20k_VCR_Berm1pt9m_Slope0pt04.csv",  # can by .py or .csv
        mean_yearly_storms=8.3,
        SD_yearly_storms=5.9,
        MHW=0.46,  # m NAVD88
        StormStart=2,
        BermEl=1.9,  # m NAVD88, just used for plotting
        model_years=10000,
        bPlot=True,
        bSave=True,
        output_filename="StormSeries_10kyrs_VCR_Berm1pt9m_Slope0pt04_02",
    )

    StormSeries_NormDist_10kyrs_03 = yearly_storms(
        datadir=datadir,
        storm_list_name="StormList_20k_VCR_Berm1pt9m_Slope0pt04.csv",  # can by .py or .csv
        mean_yearly_storms=8.3,
        SD_yearly_storms=5.9,
        MHW=0.46,  # m NAVD88
        StormStart=2,
        BermEl=1.9,  # m NAVD88, just used for plotting
        model_years=10000,
        bPlot=True,
        bSave=True,
        output_filename="StormSeries_10kyrs_VCR_Berm1pt9m_Slope0pt04_03",
    )

    StormSeries_NormDist_10kyrs_04 = yearly_storms(
        datadir=datadir,
        storm_list_name="StormList_20k_VCR_Berm1pt9m_Slope0pt04.csv",  # can by .py or .csv
        mean_yearly_storms=8.3,
        SD_yearly_storms=5.9,
        MHW=0.46,  # m NAVD88
        StormStart=2,
        BermEl=1.9,  # m NAVD88, just used for plotting
        model_years=10000,
        bPlot=True,
        bSave=True,
        output_filename="StormSeries_10kyrs_VCR_Berm1pt9m_Slope0pt04_04",
    )

    StormSeries_NormDist_10kyrs_05 = yearly_storms(
        datadir=datadir,
        storm_list_name="StormList_20k_VCR_Berm1pt9m_Slope0pt04.csv",  # can by .py or .csv
        mean_yearly_storms=8.3,
        SD_yearly_storms=5.9,
        MHW=0.46,  # m NAVD88
        StormStart=2,
        BermEl=1.9,  # m NAVD88, just used for plotting
        model_years=10000,
        bPlot=True,
        bSave=True,
        output_filename="StormSeries_10kyrs_VCR_Berm1pt9m_Slope0pt04_05",
    )

    StormSeries_NormDist_1kyrs_01 = yearly_storms(
        datadir=datadir,
        storm_list_name="StormList_20k_VCR_Berm1pt9m_Slope0pt04.csv",  # can by .py or .csv
        mean_yearly_storms=8.3,
        SD_yearly_storms=5.9,
        MHW=0.46,  # m NAVD88
        StormStart=2,
        BermEl=1.9,  # m NAVD88, just used for plotting
        model_years=1000,
        bPlot=True,
        bSave=True,
        output_filename="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01",
    )

    StormSeries_NormDist_1kyrs_02 = yearly_storms(
        datadir=datadir,
        storm_list_name="StormList_20k_VCR_Berm1pt9m_Slope0pt04.csv",  # can by .py or .csv
        mean_yearly_storms=8.3,
        SD_yearly_storms=5.9,
        MHW=0.46,  # m NAVD88
        StormStart=2,
        BermEl=1.9,  # m NAVD88, just used for plotting
        model_years=1000,
        bPlot=True,
        bSave=True,
        output_filename="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_02",
    )

    def one_hundred_increase_storm_intensity_and_frequency():
        number_storms = 105
        datadir = "cascade/data/pathways_data/"

        # for iStorm in range(number_storms):
        for iStorm in range(100, 105):

            output_filename = (
                "StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_FutureScenario"
                + str(iStorm)
            )
            shift_storm_intensity(
                datadir=datadir,
                storm_list_name="StormList_20k_VCR_Berm1pt9m_Slope0pt04.csv",  # can by .py or .csv
                mean_yearly_storms=12,
                SD_yearly_storms=5.9,
                shift=0.15,  # shift the TWL distribution to change intensity, m NAVD88; [-0.15, 0.15] for Reeves et al., 2021
                MHW=0.46,  # m NAVD88
                StormStart=2,
                BermEl=1.9,  # m NAVD88, just used for plotting
                model_years=1000,
                bPlot=False,
                bSave=True,
                output_filename=output_filename,
            )

    def one_hundered_ish_1kyr_storms():
        number_storms = 100
        datadir = "cascade/data/pathways_data/"

        for iStorm in range(number_storms):

            output_filename = "StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_" + str(
                iStorm
            )
            yearly_storms(
                datadir=datadir,
                storm_list_name="StormList_20k_VCR_Berm1pt9m_Slope0pt04.csv",  # can by .py or .csv
                mean_yearly_storms=8.3,
                SD_yearly_storms=5.9,
                MHW=0.46,  # m NAVD88
                StormStart=2,
                BermEl=1.9,  # m NAVD88, just used for plotting
                model_years=1000,
                bPlot=False,
                bSave=True,
                output_filename=output_filename,
            )

    def BermEl_2m_sensitivity_test():
        name = "StormTimeSeries_10k-yr.npy"
        yearly_storms(
            datadir=datadir,
            name=name,
            storm_list_name="VCRStormList.npy",
            mean_storm=8.3,
            SD_storm=5.9,
            MHW=0.46,
            StormStart=2,
            BermEl=1.9,
            model_years=10000,  # note, this is the number of storms contained in the MSSM model. probably should make more.
        )

        name = "StormTimeSeries_3000yr.npy"
        yearly_storms(
            datadir=datadir,
            name=name,
            storm_list_name="VCRStormList.npy",
            mean_storm=8.3,
            SD_storm=5.9,
            MHW=0.46,
            StormStart=2,
            BermEl=1.9,
            model_years=3000,
        )

        name = "StormTimeSeries_1000yr.npy"
        yearly_storms(
            datadir=datadir,
            name=name,
            storm_list_name="VCRStormList.npy",
            mean_storm=8.3,
            SD_storm=5.9,
            MHW=0.46,
            StormStart=2,
            BermEl=1.9,
            model_years=1000,
        )

        name = "StormTimeSeries_200yr.npy"
        yearly_storms(
            datadir=datadir,
            name=name,
            storm_list_name="VCRStormList.npy",
            mean_storm=8.3,
            SD_storm=5.9,
            MHW=0.46,
            StormStart=2,
            BermEl=1.9,
            model_years=200,
        )

    name = "DuneStart_1000dam.npy"
    gen_dune_height_start(datadir, name, Dstart=0.5, ny=1000)

    name = "growthparam_1000dam.npy"
    gen_alongshore_variable_rmin_rmax(datadir, name, rmin=0.35, rmax=0.85, ny=1000)

# 10,000 year simulations -------------------------------------------------------
def cascade_10kyr_sensitivity():

    cascade_10kyr_pt45_01 = RUN_4_CASCADE_noAST_Rave_SLR_pt004_NoHumans(
        nt=10000,
        rmin=0.25,  # rave = 0.45 (but not 0.5 spaced like in Reeves et al., 2021 -- arbitrary)
        rmax=0.65,
        name="4-B3D_noAST_Rave_pt45_SLR_pt004_10k-yrs_01",
        storm_file="StormSeries_10kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",  # used cascade_default_storm_list.csv
        elevation_file="barrier3d-default-elevation.npy",
        dune_file="pathways-dunes.npy",
    )

    cascade_10kyr_pt45_02 = RUN_4_CASCADE_noAST_Rave_SLR_pt004_NoHumans(
        nt=10000,
        rmin=0.25,  # rave = 0.45
        rmax=0.65,
        name="4-B3D_noAST_Rave_pt45_SLR_pt004_10k-yrs_02",
        storm_file="StormSeries_10kyrs_VCR_Berm1pt9m_Slope0pt04_02.npy",
        elevation_file="barrier3d-default-elevation.npy",
        dune_file="pathways-dunes.npy",
    )

    cascade_10kyr_pt45_03 = RUN_4_CASCADE_noAST_Rave_SLR_pt004_NoHumans(
        nt=10000,
        rmin=0.25,  # rave = 0.45
        rmax=0.65,
        name="4-B3D_noAST_Rave_pt45_SLR_pt004_10k-yrs_03",
        storm_file="StormSeries_10kyrs_VCR_Berm1pt9m_Slope0pt04_03.npy",
        elevation_file="barrier3d-default-elevation.npy",
        dune_file="pathways-dunes.npy",
    )

    cascade_10kyr_pt45_04 = RUN_4_CASCADE_noAST_Rave_SLR_pt004_NoHumans(
        nt=10000,
        rmin=0.25,  # rave = 0.45
        rmax=0.65,
        name="4-B3D_noAST_Rave_pt45_SLR_pt004_10k-yrs_04",
        storm_file="StormSeries_10kyrs_VCR_Berm1pt9m_Slope0pt04_04.npy",
        elevation_file="barrier3d-default-elevation.npy",
        dune_file="pathways-dunes.npy",
    )

    cascade_10kyr_pt45_05 = RUN_4_CASCADE_noAST_Rave_SLR_pt004_NoHumans(
        nt=10000,
        rmin=0.25,  # rave = 0.45
        rmax=0.65,
        name="4-B3D_noAST_Rave_pt45_SLR_pt004_10k-yrs_05",
        storm_file="StormSeries_10kyrs_VCR_Berm1pt9m_Slope0pt04_05.npy",
        elevation_file="barrier3d-default-elevation.npy",
        dune_file="pathways-dunes.npy",
    )

    cascade_10kyr_pt75_01 = RUN_4_CASCADE_noAST_Rave_SLR_pt004_NoHumans(
        nt=10000,
        rmin=0.55,  # rave = 0.75
        rmax=0.95,
        name="4-B3D_noAST_Rave_pt75_SLR_pt004_10k-yrs_01",
        storm_file="StormSeries_10kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
        elevation_file="barrier3d-default-elevation.npy",
        dune_file="pathways-dunes.npy",
    )

    cascade_10kyr_pt75_02 = RUN_4_CASCADE_noAST_Rave_SLR_pt004_NoHumans(
        nt=10000,
        rmin=0.55,  # rave = 0.75
        rmax=0.95,
        name="4-B3D_noAST_Rave_pt75_SLR_pt004_10k-yrs_02",
        storm_file="StormSeries_10kyrs_VCR_Berm1pt9m_Slope0pt04_02.npy",
        elevation_file="barrier3d-default-elevation.npy",
        dune_file="pathways-dunes.npy",
    )

    cascade_10kyr_pt75_03 = RUN_4_CASCADE_noAST_Rave_SLR_pt004_NoHumans(
        nt=10000,
        rmin=0.55,  # rave = 0.75
        rmax=0.95,
        name="4-B3D_noAST_Rave_pt75_SLR_pt004_10k-yrs_03",
        storm_file="StormSeries_10kyrs_VCR_Berm1pt9m_Slope0pt04_03.npy",
        elevation_file="barrier3d-default-elevation.npy",
        dune_file="pathways-dunes.npy",
    )

    cascade_10kyr_pt75_04 = RUN_4_CASCADE_noAST_Rave_SLR_pt004_NoHumans(
        nt=10000,
        rmin=0.55,  # rave = 0.75
        rmax=0.95,
        name="4-B3D_noAST_Rave_pt75_SLR_pt004_10k-yrs_04",
        storm_file="StormSeries_10kyrs_VCR_Berm1pt9m_Slope0pt04_04.npy",
        elevation_file="barrier3d-default-elevation.npy",
        dune_file="pathways-dunes.npy",
    )

    cascade_10kyr_pt75_05 = RUN_4_CASCADE_noAST_Rave_SLR_pt004_NoHumans(
        nt=10000,
        rmin=0.55,  # rave = 0.75
        rmax=0.95,
        name="4-B3D_noAST_Rave_pt75_SLR_pt004_10k-yrs_05",
        storm_file="StormSeries_10kyrs_VCR_Berm1pt9m_Slope0pt04_05.npy",
        elevation_file="barrier3d-default-elevation.npy",
        dune_file="pathways-dunes.npy",
    )

    def sensitivity_tests_Ian_model():
        cascade_10kyr_pt75_Cbbr0pt5 = RUN_4_CASCADE_noAST_Rave_SLR_pt004_NoHumans(
            nt=10000,
            rmin=0.55,  # rave = 0.75
            rmax=0.95,
            name="4-CASCADE_noAST_Rave_pt75_SLR_pt004_10k-yrs_Cbb0pt5",
            storm_file="StormSeries_10kyrs_VCR_Berm1pt9m_Slope0pt04.npy",
            elevation_file="InitElevHog.npy",
            dune_file="DuneStart_1000dam.npy",
        )

        cascade_10kyr_pt75_old_storms = RUN_4_CASCADE_noAST_Rave_SLR_pt004_NoHumans(
            nt=10000,
            rmin=0.55,  # rave = 0.75
            rmax=0.95,
            name="4-CASCADE_noAST_Rave_pt75_SLR_pt004_10k-yrs_OLD_STORMS",
            storm_file="Default_StormTimeSeries_10k-yr.npy",
            elevation_file="InitElevHog.npy",
            dune_file="DuneStart_1000dam.npy",
        )

        cascade_10kyr_pt75_old_storms_Cbbr0pt5 = (
            RUN_4_CASCADE_noAST_Rave_SLR_pt004_NoHumans(
                nt=10000,
                rmin=0.55,  # rave = 0.75
                rmax=0.95,
                name="4-CASCADE_noAST_Rave_pt75_SLR_pt004_10k-yrs_OLD_STORMS_Cbb0pt5",
                storm_file="Default_StormTimeSeries_10k-yr.npy",
                elevation_file="InitElevHog.npy",
                dune_file="DuneStart_1000dam.npy",
            )
        )

        # manually changed the berm elevation to 2.0 in the yaml
        cascade_10kyr_pt75_old_storms_BermEl2 = (
            RUN_4_CASCADE_noAST_Rave_SLR_pt004_NoHumans(
                nt=10000,
                rmin=0.55,  # rave = 0.75
                rmax=0.95,
                name="4-CASCADE_noAST_Rave_pt75_SLR_pt004_10k-yrs_OLD_STORMS_BermEl2",
                storm_file="Default_StormTimeSeries_10k-yr.npy",
                elevation_file="InitElevHog.npy",
                dune_file="DuneStart_1000dam.npy",
            )
        )

# 1,000 year simulations -------------------------------------------------------------------
def SLR_sensitivity():
        """
        Completed runs using new elevations on 6/30/222 and 7/24-25/22
        """
        cascade_pt75_low_SLR0pt008 = RUN_7_CASCADE_noAST_Rave_variableSLR_NoHumans(
            nt=200,
            rmin=0.55,
            rmax=0.95,  # rave = 0.75
            name="7-B3D_Rave_pt75_Natural_low_0pt008SLR",
            storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
            elevation_file="b3d_pt75_4261yrs_low-elevations.csv",
            dune_file="pathways-dunes.npy",
            sea_level_rise_rate=0.008,  # m/yr
            sea_level_constant=True,
        )

        cascade_pt75_low_SLR0pt012 = RUN_7_CASCADE_noAST_Rave_variableSLR_NoHumans(
            nt=200,
            rmin=0.55,
            rmax=0.95,  # rave = 0.75
            name="7-B3D_Rave_pt75_Natural_low_0pt012SLR",
            storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
            elevation_file="b3d_pt75_4261yrs_low-elevations.csv",
            dune_file="pathways-dunes.npy",
            sea_level_rise_rate=0.012,  # m/yr
            sea_level_constant=True,
        )

        cascade_pt75_high_SLR0pt008 = RUN_7_CASCADE_noAST_Rave_variableSLR_NoHumans(
            nt=200,
            rmin=0.55,
            rmax=0.95,  # rave = 0.75
            name="7-B3D_Rave_pt75_Natural_high_0pt008SLR",
            storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
            elevation_file="b3d_pt75_829yrs_high-elevations.csv",
            dune_file="pathways-dunes.npy",
            sea_level_rise_rate=0.008,  # m/yr
            sea_level_constant=True,
        )

        cascade_pt75_high_SLR0pt012 = RUN_7_CASCADE_noAST_Rave_variableSLR_NoHumans(
            nt=200,
            rmin=0.55,
            rmax=0.95,  # rave = 0.75
            name="7-B3D_Rave_pt75_Natural_high_0pt012SLR",
            storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
            elevation_file="b3d_pt75_829yrs_high-elevations.csv",
            dune_file="pathways-dunes.npy",
            sea_level_rise_rate=0.012,  # m/yr
            sea_level_constant=True,
        )

        cascade_pt45_low_SLR0pt008 = RUN_7_CASCADE_noAST_Rave_variableSLR_NoHumans(
            nt=200,
            rmin=0.25,
            rmax=0.65,  # rave = 0.45
            name="7-B3D_Rave_pt45_Natural_low_0pt008SLR",
            storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
            elevation_file="b3d_pt45_8757yrs_low-elevations.csv",
            dune_file="pathways-dunes.npy",
            sea_level_rise_rate=0.008,  # m/yr
            sea_level_constant=True,
        )

        cascade_pt45_low_SLR0pt012 = RUN_7_CASCADE_noAST_Rave_variableSLR_NoHumans(
            nt=200,
            rmin=0.25,
            rmax=0.65,  # rave = 0.45
            name="7-B3D_Rave_pt45_Natural_low_0pt012SLR",
            storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
            elevation_file="b3d_pt45_8757yrs_low-elevations.csv",
            dune_file="pathways-dunes.npy",
            sea_level_rise_rate=0.012,  # m/yr
            sea_level_constant=True,
        )

        cascade_pt45_high_SLR0pt008 = RUN_7_CASCADE_noAST_Rave_variableSLR_NoHumans(
            nt=200,
            rmin=0.25,
            rmax=0.65,  # rave = 0.45
            name="7-B3D_Rave_pt45_Natural_high_0pt008SLR",
            storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
            elevation_file="b3d_pt45_802yrs_high-elevations.csv",
            dune_file="pathways-dunes.npy",
            sea_level_rise_rate=0.008,  # m/yr
            sea_level_constant=True,
        )

        cascade_pt45_high_SLR0pt012 = RUN_7_CASCADE_noAST_Rave_variableSLR_NoHumans(
            nt=200,
            rmin=0.25,
            rmax=0.65,  # rave = 0.45
            name="7-B3D_Rave_pt45_Natural_high_0pt012SLR",
            storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
            elevation_file="b3d_pt45_802yrs_high-elevations.csv",
            dune_file="pathways-dunes.npy",
            sea_level_rise_rate=0.012,  # m/yr
            sea_level_constant=True,
        )

        # start of accelerated SLR scenarios
        # for the accelerated SLR scenario, I had to hard code the parameters that correspond to the
        # Rohling et al. (2013) 68% upper bound for AD2000-2200. SLRR starts at 0.003 m/yr and ends at 0.022 m/yr;
        # matches with the bounds of RCP8.5 SLR by 2100 and 2200
        cascade_pt75_low_SLRacc = RUN_7_CASCADE_noAST_Rave_variableSLR_NoHumans(
            nt=200,
            rmin=0.55,
            rmax=0.95,  # rave = 0.75
            name="7-B3D_Rave_pt75_Natural_low_AccSLR",
            storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
            elevation_file="b3d_pt75_4261yrs_low-elevations.csv",
            dune_file="pathways-dunes.npy",
            sea_level_rise_rate=0.008,  # dummy
            sea_level_constant=False,  # accelerated
        )

        cascade_pt75_high_SLRacc = RUN_7_CASCADE_noAST_Rave_variableSLR_NoHumans(
            nt=200,
            rmin=0.55,
            rmax=0.95,  # rave = 0.75
            name="7-B3D_Rave_pt75_Natural_high_AccSLR",
            storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
            elevation_file="b3d_pt75_829yrs_high-elevations.csv",
            dune_file="pathways-dunes.npy",
            sea_level_rise_rate=0.008,  # m/yr
            sea_level_constant=False,
        )

        cascade_pt45_low_SLRacc = RUN_7_CASCADE_noAST_Rave_variableSLR_NoHumans(
            nt=200,
            rmin=0.25,
            rmax=0.65,  # rave = 0.45
            name="7-B3D_Rave_pt45_Natural_low_AccSLR",
            storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
            elevation_file="b3d_pt45_8757yrs_low-elevations.csv",
            dune_file="pathways-dunes.npy",
            sea_level_rise_rate=0.012,  # m/yr
            sea_level_constant=False,
        )

        cascade_pt45_high_SLRacc = RUN_7_CASCADE_noAST_Rave_variableSLR_NoHumans(
            nt=200,
            rmin=0.25,
            rmax=0.65,  # rave = 0.45
            name="7-B3D_Rave_pt45_Natural_high_AccSLR",
            storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
            elevation_file="b3d_pt45_802yrs_high-elevations.csv",
            dune_file="pathways-dunes.npy",
            sea_level_rise_rate=0.008,  # m/yr
            sea_level_constant=False,
        )

def natural():
        """
        Completed runs using new elevations on 6/30/222
        """
        cascade_pt75_low = RUN_4_CASCADE_noAST_Rave_SLR_pt004_NoHumans(
            nt=1000,
            rmin=0.55,
            rmax=0.95,  # rave = 0.75
            name="4-B3D_Rave_pt75_Natural_low",
            storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
            elevation_file="b3d_pt75_4261yrs_low-elevations.csv",
            dune_file="pathways-dunes.npy",
        )

        cascade_pt75_high = RUN_4_CASCADE_noAST_Rave_SLR_pt004_NoHumans(
            nt=1000,
            rmin=0.55,
            rmax=0.95,  # rave = 0.75
            name="4-B3D_Rave_pt75_Natural_high",
            storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
            elevation_file="b3d_pt75_829yrs_high-elevations.csv",
            dune_file="pathways-dunes.npy",
        )

        cascade_pt45_low = RUN_4_CASCADE_noAST_Rave_SLR_pt004_NoHumans(
            nt=1000,
            rmin=0.25,
            rmax=0.65,  # rave = 0.45
            name="4-B3D_Rave_pt45_Natural_low",
            storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
            elevation_file="b3d_pt45_8757yrs_low-elevations.csv",
            dune_file="pathways-dunes.npy",
        )

        cascade_pt45_high = RUN_4_CASCADE_noAST_Rave_SLR_pt004_NoHumans(
            nt=1000,
            rmin=0.25,
            rmax=0.65,  # rave = 0.45
            name="4-B3D_Rave_pt45_Natural_high",
            storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
            elevation_file="b3d_pt45_802yrs_high-elevations.csv",
            dune_file="pathways-dunes.npy",
        )

        def averages():
            def one_hundred_natural_runs(
                name_prefix, rmin, rmax, elevation_file, year_start, year_end
            ):

                for iStorm in range(year_start, year_end):
                    name = name_prefix + str(iStorm)
                    storm_file = (
                        "StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_"
                        + str(iStorm)
                        + ".npy"
                    )

                    RUN_4_CASCADE_noAST_Rave_SLR_pt004_NoHumans(
                        nt=1000,
                        rmin=rmin,
                        rmax=rmax,
                        name=name,
                        storm_file=storm_file,
                        elevation_file=elevation_file,
                        dune_file="pathways-dunes.npy",
                    )

            one_hundred_natural_runs(
                name_prefix="4-B3D_Rave_pt45_Natural_low",
                rmin=0.25,
                rmax=0.65,
                elevation_file="b3d_pt45_8757yrs_low-elevations.csv",
                year_start=22,
                year_end=100,
            )

            one_hundred_natural_runs(
                name_prefix="4-B3D_Rave_pt45_Natural_high",
                rmin=0.25,
                rmax=0.65,
                elevation_file="b3d_pt45_802yrs_high-elevations.csv",
                year_start=22,
                year_end=100,
            )

            one_hundred_natural_runs(
                name_prefix="4-B3D_Rave_pt75_Natural_low",
                rmin=0.55,
                rmax=0.95,  # rave = 0.75
                elevation_file="b3d_pt75_4261yrs_low-elevations.csv",
                year_start=0,
                year_end=50,
            )

            one_hundred_natural_runs(
                name_prefix="4-B3D_Rave_pt75_Natural_high",
                rmin=0.55,
                rmax=0.95,  # rave = 0.75
                elevation_file="b3d_pt75_829yrs_high-elevations.csv",
                year_start=92,
                year_end=100,
            )

def roadways():
        def pt75():
            def low():
                # Barrier has HEIGHT DROWNED at t = 136 years
                cascade_pt75_h1m_low = RUN_6_CASCADE_noAST_Rave_SLR_pt004_Roadways(
                    nt=1000,
                    rmin=0.55,
                    rmax=0.95,  # rave = 0.75
                    name="6-B3D_Rave_pt75_Roadways_1mDune_20mSetback_20mWidth_low",
                    road_ele=0.6,  # average initial elevation, 0.575 m MHW
                    road_width=20,  # m
                    road_setback=20,  # m
                    dune_design_elevation=1.6,  # m MHW, rebuild to 1 m dune above the roadway
                    dune_minimum_elevation=1.1,  # m MHW, allow dune to erode down to 0.5 m above the roadway
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt75_4261yrs_low-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    background_erosion=0.0,
                )

                # Barrier has HEIGHT DROWNED at t = 136 years
                cascade_pt75_h2m_low = RUN_6_CASCADE_noAST_Rave_SLR_pt004_Roadways(
                    nt=1000,
                    rmin=0.55,
                    rmax=0.95,  # rave = 0.75
                    name="6-B3D_Rave_pt75_Roadways_2mDune_20mSetback_20mWidth_low",
                    road_ele=0.6,
                    road_width=20,  # m
                    road_setback=20,  # m
                    dune_design_elevation=2.6,  # m MHW, rebuild to 2 m dune above the roadway
                    dune_minimum_elevation=1.1,  # m MHW, allow dune to erode down to 0.5 m above the roadway
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt75_4261yrs_low-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    background_erosion=0.0,
                )

                # Island is too narrow for roadway to be relocated. Roadway eaten up by dunes at 73 years
                cascade_pt75_h2m_low_BE1m = RUN_6_CASCADE_noAST_Rave_SLR_pt004_Roadways(
                    nt=1000,
                    rmin=0.55,
                    rmax=0.95,  # rave = 0.75
                    name="6-B3D_Rave_pt75_Roadways_2mDune_20mSetback_20mWidth_low_BE1m",
                    road_ele=0.6,
                    road_width=20,  # m
                    road_setback=20,  # m
                    dune_design_elevation=2.6,  # m MHW, rebuild to 2 m dune above the roadway
                    dune_minimum_elevation=1.1,  # m MHW, allow dune to erode down to 0.5 m above the roadway
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt75_4261yrs_low-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    background_erosion=-1,
                )

                # Barrier has HEIGHT DROWNED at t = 132 years
                cascade_pt75_h3m_low = RUN_6_CASCADE_noAST_Rave_SLR_pt004_Roadways(
                    nt=1000,
                    rmin=0.55,
                    rmax=0.95,  # rave = 0.75
                    name="6-B3D_Rave_pt75_Roadways_3mDune_20mSetback_20mWidth_low",
                    road_ele=0.6,
                    road_width=20,  # m
                    road_setback=20,  # m
                    dune_design_elevation=3.6,  # m MHW, rebuild to 3 m dune above the roadway
                    dune_minimum_elevation=1.1,  # m MHW, allow dune to erode down to 0.5 m above the roadway
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt75_4261yrs_low-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    background_erosion=0.0,
                )

            def high():
                # Roadway width drowned at 535 years, 20.0% of road borders water
                cascade_pt75_h1m_high = RUN_6_CASCADE_noAST_Rave_SLR_pt004_Roadways(
                    nt=1000,
                    rmin=0.55,
                    rmax=0.95,  # rave = 0.75
                    name="6-B3D_Rave_pt75_Roadways_1mDune_20mSetback_20mWidth_high",
                    road_ele=2.1,  # average initial elevation, 2.14 m MHW
                    road_width=20,  # m
                    road_setback=20,  # m
                    dune_design_elevation=3.1,  # m MHW, rebuild to 1 m dune above the roadway
                    dune_minimum_elevation=2.6,  # m MHW, allow dune to erode down to 0.5 m above the roadway
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt75_829yrs_high-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    background_erosion=0.0,
                )

                # Roadway width drowned at 520 years, 20.0% of road borders water
                # Barrier has HEIGHT DROWNED at t = 571 years
                cascade_pt75_h2m_high = RUN_6_CASCADE_noAST_Rave_SLR_pt004_Roadways(
                    nt=1000,
                    rmin=0.55,
                    rmax=0.95,  # rave = 0.75
                    name="6-B3D_Rave_pt75_Roadways_2mDune_20mSetback_20mWidth_high",
                    road_ele=2.1,
                    road_width=20,  # m
                    road_setback=20,  # m
                    dune_design_elevation=4.1,  # m MHW, rebuild to 2 m dune above the roadway
                    dune_minimum_elevation=2.6,  # m MHW, allow dune to erode down to 0.5 m above the roadway
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt75_829yrs_high-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    background_erosion=0.0,
                )

                # Island is to narrow for roadway to be relocated. Roadway eaten up by dunes at 395 years
                cascade_pt75_h3m_high = RUN_6_CASCADE_noAST_Rave_SLR_pt004_Roadways(
                    nt=1000,
                    rmin=0.55,
                    rmax=0.95,  # rave = 0.75
                    name="6-B3D_Rave_pt75_Roadways_3mDune_20mSetback_20mWidth_high",
                    road_ele=2.1,
                    road_width=20,  # m
                    road_setback=20,  # m
                    dune_design_elevation=5.1,  # m MHW, rebuild to 3 m dune above the roadway
                    dune_minimum_elevation=2.6,  # m MHW, allow dune to erode down to 0.5 m above the roadway
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt75_829yrs_high-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    background_erosion=0.0,
                )

        def pt45():
            def low():
                def averages():
                    def one_hundred_roadway_runs(
                        name_prefix, year_start, year_end, dune_design_elevation
                    ):
                        for iStorm in range(year_start, year_end):
                            name = name_prefix + str(iStorm)
                            storm_file = (
                                "StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_"
                                + str(iStorm)
                                + ".npy"
                            )

                            RUN_6_CASCADE_noAST_Rave_SLR_pt004_Roadways(
                                nt=1000,
                                rmin=0.25,
                                rmax=0.65,  # rave = 0.45
                                name=name,
                                road_ele=1.6,  # average initial elevation 1.64 m MHW
                                road_width=20,  # m
                                road_setback=20,  # m
                                dune_design_elevation=dune_design_elevation,  # m MHW, rebuild to 1 m dune above the roadway
                                dune_minimum_elevation=2.1,
                                # m MHW, allow dune to erode down to 0.5 m above the roadway
                                storm_file=storm_file,
                                elevation_file="b3d_pt45_8757yrs_low-elevations.csv",
                                dune_file="pathways-dunes.npy",
                                background_erosion=0.0,
                            )

                    one_hundred_roadway_runs(
                        name_prefix="6-B3D_Rave_pt45_Roadways_1mDune_20mSetback_20mWidth_low",
                        year_start=0,
                        year_end=100,
                        dune_design_elevation=2.6,
                    )

                    one_hundred_roadway_runs(
                        name_prefix="6-B3D_Rave_pt45_Roadways_2mDune_20mSetback_20mWidth_low",
                        year_start=0,
                        year_end=100,
                        dune_design_elevation=3.6,
                    )

                    one_hundred_roadway_runs(
                        name_prefix="6-B3D_Rave_pt45_Roadways_3mDune_20mSetback_20mWidth_low",
                        year_start=0,
                        year_end=100,
                        dune_design_elevation=4.6,
                    )

                # Roadway width drowned at 544 years, 20.0% of road borders water
                cascade_pt45_h1m_low = RUN_6_CASCADE_noAST_Rave_SLR_pt004_Roadways(
                    nt=1000,
                    rmin=0.25,
                    rmax=0.65,  # rave = 0.45
                    name="6-B3D_Rave_pt45_Roadways_1mDune_20mSetback_20mWidth_low",
                    road_ele=1.6,  # average initial elevation 1.64 m MHW
                    road_width=20,  # m
                    road_setback=20,  # m
                    dune_design_elevation=2.6,  # m MHW, rebuild to 1 m dune above the roadway
                    dune_minimum_elevation=2.1,  # m MHW, allow dune to erode down to 0.5 m above the roadway
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt45_8757yrs_low-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    background_erosion=0.0,
                )

                # Roadway width drowned at 533 years, 20.0% of road borders water
                cascade_pt45_h2m_low = RUN_6_CASCADE_noAST_Rave_SLR_pt004_Roadways(
                    nt=1000,
                    rmin=0.25,
                    rmax=0.65,  # rave = 0.45
                    name="6-B3D_Rave_pt45_Roadways_2mDune_20mSetback_20mWidth_low",
                    road_ele=1.6,
                    road_width=20,  # m
                    road_setback=20,  # m
                    dune_design_elevation=3.6,  # m MHW, rebuild to 2 m dune above the roadway
                    dune_minimum_elevation=2.1,  # m MHW, allow dune to erode down to 0.5 m above the roadway
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt45_8757yrs_low-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    background_erosion=0.0,
                )

                # # Island is too narrow for roadway to be relocated. Roadway eaten up by dunes at 187 years
                # cascade_pt45_h2m_low_BE1m = RUN_6_CASCADE_noAST_Rave_SLR_pt004_Roadways(
                #     nt=1000,
                #     rmin=0.25,
                #     rmax=0.65,  # rave = 0.45
                #     name="6-B3D_Rave_pt45_Roadways_2mDune_20mSetback_20mWidth_low_BE1m",
                #     road_ele=1.6,
                #     road_width=20,  # m
                #     road_setback=20,  # m
                #     dune_design_elevation=3.6,  # m MHW, rebuild to 2 m dune above the roadway
                #     dune_minimum_elevation=2.1,  # m MHW, allow dune to erode down to 0.5 m above the roadway
                #     storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                #     elevation_file="b3d_pt45_8757yrs_low-elevations.csv",
                #     dune_file="pathways-dunes.npy",
                #     background_erosion=-1,
                # )

                # Roadway width drowned at 322 years, 20.0% of road borders water
                cascade_pt45_h3m_low = RUN_6_CASCADE_noAST_Rave_SLR_pt004_Roadways(
                    nt=1000,
                    rmin=0.25,
                    rmax=0.65,  # rave = 0.45
                    name="6-B3D_Rave_pt45_Roadways_3mDune_20mSetback_20mWidth_low",
                    road_ele=1.6,
                    road_width=20,  # m
                    road_setback=20,  # m
                    dune_design_elevation=4.6,  # m MHW, rebuild to 3 m dune above the roadway
                    dune_minimum_elevation=2.1,  # m MHW, allow dune to erode down to 0.5 m above the roadway
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt45_8757yrs_low-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    background_erosion=0.0,
                )

            def high():
                # Island is too narrow for roadway to be relocated. Roadway eaten up by dunes at 650 years
                cascade_pt45_h1m_high = RUN_6_CASCADE_noAST_Rave_SLR_pt004_Roadways(
                    nt=1000,
                    rmin=0.25,
                    rmax=0.65,  # rave = 0.45
                    name="6-B3D_Rave_pt45_Roadways_1mDune_20mSetback_20mWidth_high",
                    road_ele=1.8,  # initial average, 1.83 m MHW
                    road_width=20,  # m
                    road_setback=20,  # m
                    dune_design_elevation=2.8,  # m MHW, rebuild to 1 m dune above the roadway
                    dune_minimum_elevation=2.3,  # m MHW, allow dune to erode down to 0.5 m above the roadway
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt45_802yrs_high-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    background_erosion=0.0,
                )

                # Roadway width drowned at 628 years, 20.0% of road borders water
                cascade_pt45_h2m_high = RUN_6_CASCADE_noAST_Rave_SLR_pt004_Roadways(
                    nt=1000,
                    rmin=0.25,
                    rmax=0.65,  # rave = 0.45
                    name="6-B3D_Rave_pt45_Roadways_2mDune_20mSetback_20mWidth_high",
                    road_ele=1.8,
                    road_width=20,  # m
                    road_setback=20,  # m
                    dune_design_elevation=3.8,  # m MHW, rebuild to 2 m dune above the roadway
                    dune_minimum_elevation=2.3,  # m MHW, allow dune to erode down to 0.5 m above the roadway
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt45_802yrs_high-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    background_erosion=0.0,
                )

                # Roadway width drowned at 522 years, 20.0% of road borders water
                cascade_pt45_h3m_high = RUN_6_CASCADE_noAST_Rave_SLR_pt004_Roadways(
                    nt=1000,
                    rmin=0.25,
                    rmax=0.65,  # rave = 0.45
                    name="6-B3D_Rave_pt45_Roadways_3mDune_20mSetback_20mWidth_high",
                    road_ele=1.8,
                    road_width=20,  # m
                    road_setback=20,  # m
                    dune_design_elevation=4.8,  # m MHW, rebuild to 3 m dune above the roadway
                    dune_minimum_elevation=2.3,  # m MHW, allow dune to erode down to 0.5 m above the roadway
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt45_802yrs_high-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    background_erosion=0.0,
                )

        def roadway_sensitivity_abandonment_criteria():

            # test the sensitivity of varying the number of water cells that border the roadway as a metric to stop
            # managing the road for the most extreme barrier trajectory (high dune growth rate, low barrier)

            # Roadway width drowned at 462 years, 10.0% of road borders water
            cascade_pt45_h2m_low_10percent = RUN_6_CASCADE_noAST_Rave_SLR_pt004_Roadways(
                nt=1000,
                rmin=0.25,
                rmax=0.65,  # rave = 0.45
                name="6-B3D_Rave_pt45_Roadways_2mDune_20mSetback_20mWidth_low_10percent",
                road_ele=1.6,  # average initial elevation, 0.575 m MHW
                road_width=20,  # m
                road_setback=20,  # m
                dune_design_elevation=3.6,  # m MHW, rebuild to 2 m dune above the roadway
                dune_minimum_elevation=2.1,  # m MHW, allow dune to erode down to 0.5 m above the roadway
                storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                elevation_file="b3d_pt45_8757yrs_low-elevations.csv",
                dune_file="pathways-dunes.npy",
                background_erosion=0.0,
                percent_water_cells_sensitivity=0.1,
            )

            # Roadway width drowned at 533 years, 20.0% of road borders water
            cascade_pt45_h2m_low_20percent = RUN_6_CASCADE_noAST_Rave_SLR_pt004_Roadways(
                nt=1000,
                rmin=0.25,
                rmax=0.65,  # rave = 0.45
                name="6-B3D_Rave_pt45_Roadways_2mDune_20mSetback_20mWidth_low_20percent",
                road_ele=1.6,
                road_width=20,  # m
                road_setback=20,  # m
                dune_design_elevation=3.6,  # m MHW, rebuild to 2 m dune above the roadway
                dune_minimum_elevation=2.1,  # m MHW, allow dune to erode down to 0.5 m above the roadway
                storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                elevation_file="b3d_pt45_8757yrs_low-elevations.csv",
                dune_file="pathways-dunes.npy",
                background_erosion=0.0,
                percent_water_cells_sensitivity=0.2,
            )

            # Roadway width drowned at 545 years, 30.0% of road borders water
            cascade_pt45_h2m_low_30percent = RUN_6_CASCADE_noAST_Rave_SLR_pt004_Roadways(
                nt=1000,
                rmin=0.25,
                rmax=0.65,  # rave = 0.45
                name="6-B3D_Rave_pt45_Roadways_2mDune_20mSetback_20mWidth_low_30percent",
                road_ele=1.6,
                road_width=20,  # m
                road_setback=20,  # m
                dune_design_elevation=3.6,  # m MHW, rebuild to 2 m dune above the roadway
                dune_minimum_elevation=2.1,  # m MHW, allow dune to erode down to 0.5 m above the roadway
                storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                elevation_file="b3d_pt45_8757yrs_low-elevations.csv",
                dune_file="pathways-dunes.npy",
                background_erosion=0.0,
                percent_water_cells_sensitivity=0.3,
            )

            # Roadway width drowned at 548 years, 40.0% of road borders water
            cascade_pt45_h2m_low_40percent = RUN_6_CASCADE_noAST_Rave_SLR_pt004_Roadways(
                nt=1000,
                rmin=0.25,
                rmax=0.65,  # rave = 0.45
                name="6-B3D_Rave_pt45_Roadways_2mDune_20mSetback_20mWidth_low_40percent",
                road_ele=1.6,
                road_width=20,  # m
                road_setback=20,  # m
                dune_design_elevation=3.6,  # m MHW, rebuild to 2 m dune above the roadway
                dune_minimum_elevation=2.1,  # m MHW, allow dune to erode down to 0.5 m above the roadway
                storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                elevation_file="b3d_pt45_8757yrs_low-elevations.csv",
                dune_file="pathways-dunes.npy",
                background_erosion=0.0,
                percent_water_cells_sensitivity=0.4,
            )

            # Roadway width drowned at 553 years, 50.0% of road borders water
            cascade_pt45_h2m_low_50percent = RUN_6_CASCADE_noAST_Rave_SLR_pt004_Roadways(
                nt=1000,
                rmin=0.25,
                rmax=0.65,  # rave = 0.45
                name="6-B3D_Rave_pt45_Roadways_2mDune_20mSetback_20mWidth_low_50percent",
                road_ele=1.6,
                road_width=20,  # m
                road_setback=20,  # m
                dune_design_elevation=3.6,  # m MHW, rebuild to 2 m dune above the roadway
                dune_minimum_elevation=2.1,  # m MHW, allow dune to erode down to 0.5 m above the roadway
                storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                elevation_file="b3d_pt45_8757yrs_low-elevations.csv",
                dune_file="pathways-dunes.npy",
                background_erosion=0.0,
                percent_water_cells_sensitivity=0.5,
            )

def nourishments():

        # note, we keep all other variables the same for comparison to the roadways scenarios except we rebuild if the
        # dune is eroded to 1-m above the berm

        def rebuild_threshold_1m():
            def pt75_low():
                # Community reached minimum width, drowned at 160 years
                cascade_pt75_h2m_low_nourishment_residential_RT1m = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                    nt=1000,
                    rmin=0.55,
                    rmax=0.95,  # rave = 0.75
                    name="8-B3D_Rave_pt75_Nourishment_2mDune_lowEle_residential_rebuild1m",
                    dune_design_elevation=2.6,
                    # m MHW, keep dune design height the same as 2m dune above the initial "roadway"
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt75_4261yrs_low-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    overwash_filter=40,  # corresponds with residential
                    overwash_to_dune=9,
                    nourishment_volume=100,  # m^3/m
                    beach_width_threshold=30,  # m
                    background_erosion=0.0,
                    rebuild_dune_threshold=1,  # m above the berm elevation
                )

                # Community reached minimum width, drowned at 83 years
                cascade_pt75_h2m_low_nourishment_commercial_RT1m = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                    nt=1000,
                    rmin=0.55,
                    rmax=0.95,  # rave = 0.75
                    name="8-B3D_Rave_pt75_Nourishment_2mDune_lowEle_commercial_rebuild1m",
                    dune_design_elevation=2.6,  # m MHW, keep dune design height the same as 2 m dune above the "roadway"
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt75_4261yrs_low-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    overwash_filter=90,  # corresponds with commercial
                    overwash_to_dune=9,
                    nourishment_volume=100,  # m^3/m
                    beach_width_threshold=30,  # m
                    background_erosion=0.0,
                    rebuild_dune_threshold=1,  # m above the berm elevation
                )

                # Community reached minimum width, drowned at 83 years
                cascade_pt75_h2m_low_nourishment_commercial_BE1m_RT1m = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                    nt=1000,
                    rmin=0.55,
                    rmax=0.95,  # rave = 0.75
                    name="8-B3D_Rave_pt75_Nourishment_2mDune_lowEle_commercial_backerosion1m_rebuild1m",
                    dune_design_elevation=2.6,  # m MHW, keep dune design height the same as 2 m dune above the "roadway"
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt75_4261yrs_low-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    overwash_filter=90,  # corresponds with commercial
                    overwash_to_dune=9,
                    nourishment_volume=100,  # m^3/m
                    beach_width_threshold=30,  # m
                    background_erosion=-1.0,  # m/yr, background shoreline erosion
                    rebuild_dune_threshold=1,  # m above the berm elevation
                )

            def pt75_high():
                # Community reached minimum width, drowned at 550
                cascade_pt75_h2m_high_nourishment_residential_RT1m = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                    nt=1000,
                    rmin=0.55,
                    rmax=0.95,  # rave = 0.75
                    name="8-B3D_Rave_pt75_Nourishment_2mDune_highEle_residential_rebuild1m",
                    dune_design_elevation=4.1,
                    # m MHW, keep dune design height the same as 2m dune above the initial "roadway" for comparison
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt75_829yrs_high-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    overwash_filter=40,  # corresponds with residential
                    overwash_to_dune=9,
                    nourishment_volume=100,  # m^3/m
                    beach_width_threshold=30,  # m
                    background_erosion=0.0,
                    rebuild_dune_threshold=1,  # m above the berm elevation
                )

                # Community reached minimum width, drowned at 518; Barrier has HEIGHT DROWNED at t = 580 years
                cascade_pt75_h2m_high_nourishment_commercial_RT1m = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                    nt=1000,
                    rmin=0.55,
                    rmax=0.95,  # rave = 0.75
                    name="8-B3D_Rave_pt75_Nourishment_2mDune_highEle_commercial_rebuild1m",
                    dune_design_elevation=4.1,
                    # m MHW, keep dune design height the same as 2 m dune above the "roadway"
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt75_829yrs_high-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    overwash_filter=90,  # corresponds with commercial
                    overwash_to_dune=9,
                    nourishment_volume=100,  # m^3/m
                    beach_width_threshold=30,  # m
                    background_erosion=0.0,
                    rebuild_dune_threshold=1,  # m above the berm elevation
                )

                # Community reached minimum width, drowned at 518 years
                cascade_pt75_h2m_high_nourishment_commercial_BE1m_RT1m = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                    nt=1000,
                    rmin=0.55,
                    rmax=0.95,  # rave = 0.75
                    name="8-B3D_Rave_pt75_Nourishment_2mDune_highEle_commercial_backerosion1m_rebuild1m",
                    dune_design_elevation=4.1,
                    # m MHW, keep dune design height the same as 2 m dune above the "roadway"
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt75_829yrs_high-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    overwash_filter=90,  # corresponds with commercial
                    overwash_to_dune=9,
                    nourishment_volume=100,  # m^3/m
                    beach_width_threshold=30,  # m
                    background_erosion=-1.0,  # m/yr, background shoreline erosion
                    rebuild_dune_threshold=1,  # m above the berm elevation
                )

            def pt45_low():
                def averages():
                    def one_hundred_nourishment_runs(
                        name_prefix,
                        year_start,
                        year_end,
                        overwash_filter,
                        background_erosion,
                    ):
                        for iStorm in range(year_start, year_end):
                            name = name_prefix + str(iStorm)
                            storm_file = (
                                "StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_"
                                + str(iStorm)
                                + ".npy"
                            )

                            RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                                nt=1000,
                                rmin=0.25,
                                rmax=0.65,  # rave = 0.45
                                name=name,
                                dune_design_elevation=3.6,
                                # m MHW, keep dune design height the same as 2 m dune above the "roadway"
                                storm_file=storm_file,
                                elevation_file="b3d_pt45_8757yrs_low-elevations.csv",
                                dune_file="pathways-dunes.npy",
                                overwash_filter=overwash_filter,
                                overwash_to_dune=9,
                                nourishment_volume=100,  # m^3/m
                                beach_width_threshold=30,  # m
                                background_erosion=background_erosion,
                                rebuild_dune_threshold=1,  # m above the berm elevation
                            )

                    one_hundred_nourishment_runs(
                        name_prefix="8-B3D_Rave_pt45_Nourishment_2mDune_lowEle_residential_rebuild1m",
                        year_start=0,
                        year_end=100,
                        overwash_filter=40,
                        background_erosion=0.0,
                    )

                    one_hundred_nourishment_runs(
                        name_prefix="8-B3D_Rave_pt45_Nourishment_2mDune_lowEle_commercial_rebuild1m",
                        year_start=0,
                        year_end=100,
                        overwash_filter=90,
                        background_erosion=0.0,
                    )

                    one_hundred_nourishment_runs(
                        name_prefix="8-B3D_Rave_pt45_Nourishment_2mDune_lowEle_commercial_backerosion1m_rebuild1m",
                        year_start=0,
                        year_end=100,
                        overwash_filter=90,
                        background_erosion=-1.0,
                    )

                # Community reached minimum width, drowned at 407 years
                cascade_pt45_h2m_low_nourishment_residential_RT1m = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                    nt=1000,
                    rmin=0.25,
                    rmax=0.65,  # rave = 0.45
                    name="8-B3D_Rave_pt45_Nourishment_2mDune_lowEle_residential_rebuild1m",
                    dune_design_elevation=3.6,  # m MHW, keep dune design height the same as 2 m dune above the "roadway"
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt45_8757yrs_low-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    overwash_filter=40,
                    overwash_to_dune=9,
                    nourishment_volume=100,  # m^3/m
                    beach_width_threshold=30,  # m
                    background_erosion=0.0,
                    rebuild_dune_threshold=1,  # m above the berm elevation
                )

                # Community reached minimum width, drowned at 302 years
                cascade_pt45_h2m_low_nourishment_commercial_RT1m = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                    nt=1000,
                    rmin=0.25,
                    rmax=0.65,  # rave = 0.45
                    name="8-B3D_Rave_pt45_Nourishment_2mDune_lowEle_commercial_rebuild1m",
                    dune_design_elevation=3.6,  # m MHW, keep dune design height the same as 2 m dune above the "roadway"
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt45_8757yrs_low-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    overwash_filter=90,  # corresponds with commercial
                    overwash_to_dune=9,
                    nourishment_volume=100,  # m^3/m
                    beach_width_threshold=30,  # m
                    background_erosion=0.0,
                    rebuild_dune_threshold=1,  # m above the berm elevation
                )

                # Community reached minimum width, drowned at 302 years
                cascade_pt45_h2m_low_nourishment_commercial_BE1m_RT1m = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                    nt=1000,  # will need to run for longer later, after AGU
                    rmin=0.25,
                    rmax=0.65,  # rave = 0.45
                    name="8-B3D_Rave_pt45_Nourishment_2mDune_lowEle_commercial_backerosion1m_rebuild1m",
                    dune_design_elevation=3.6,  # m MHW, keep dune design height the same as 2 m dune above the "roadway"
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt45_8757yrs_low-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    overwash_filter=90,  # corresponds with commercial
                    overwash_to_dune=9,
                    nourishment_volume=100,  # m^3/m
                    beach_width_threshold=30,  # m
                    background_erosion=-1.0,  # m/yr, background shoreline erosion
                    rebuild_dune_threshold=1,  # m above the berm elevation
                )

            def pt45_high():
                # Community reached minimum width, drowned at 544 years; Barrier has HEIGHT DROWNED at t = 574 years
                cascade_pt45_h2m_high_nourishment_residential_RT1m = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                    nt=1000,
                    rmin=0.25,
                    rmax=0.65,  # rave = 0.45
                    name="8-B3D_Rave_pt45_Nourishment_2mDune_highEle_residential_rebuild1m",
                    dune_design_elevation=3.8,  # m MHW, keep dune design height the same as 2 m dune above the "roadway"
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt45_802yrs_high-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    overwash_filter=40,
                    overwash_to_dune=9,
                    nourishment_volume=100,  # m^3/m
                    beach_width_threshold=30,  # m
                    background_erosion=0.0,
                    rebuild_dune_threshold=1,  # m above the berm elevation
                )

                # Community reached minimum width, drowned at 429 years
                cascade_pt45_h2m_high_nourishment_commercial_RT1m = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                    nt=1000,
                    rmin=0.25,
                    rmax=0.65,  # rave = 0.45
                    name="8-B3D_Rave_pt45_Nourishment_2mDune_highEle_commercial_rebuild1m",
                    dune_design_elevation=3.8,  # m MHW, keep dune design height the same as 2 m dune above the "roadway"
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt45_802yrs_high-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    overwash_filter=90,  # corresponds with commercial
                    overwash_to_dune=9,
                    nourishment_volume=100,  # m^3/m
                    beach_width_threshold=30,  # m
                    background_erosion=0.0,
                    rebuild_dune_threshold=1,  # m above the berm elevation
                )

                # Community reached minimum width, drowned at 429 years
                cascade_pt45_h2m_high_nourishment_commercial_BE1m_RT1m = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                    nt=1000,  # will need to run for longer later, after AGU
                    rmin=0.25,
                    rmax=0.65,  # rave = 0.45
                    name="8-B3D_Rave_pt45_Nourishment_2mDune_highEle_commercial_backerosion1m_rebuild1m",
                    dune_design_elevation=3.8,  # m MHW, keep dune design height the same as 2 m dune above the "roadway"
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt45_802yrs_high-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    overwash_filter=90,  # corresponds with commercial
                    overwash_to_dune=9,
                    nourishment_volume=100,  # m^3/m
                    beach_width_threshold=30,  # m
                    background_erosion=-1.0,  # m/yr, background shoreline erosion
                    rebuild_dune_threshold=1,  # m above the berm elevation
                )

        def topo_only():
            # we only run 10 years of the following runs because we use them for plotting the initial topo figure for
            # the CNH simulations
            cascade_pt45_h2m_high_nourishment_commercial = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                nt=10,
                rmin=0.25,
                rmax=0.65,  # rave = 0.45
                name="8-B3D_Rave_pt45_Nourishment_2mDune_highEle_commercial",
                dune_design_elevation=3.8,  # m MHW, keep dune design height the same as 2 m dune above the "roadway"
                storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                elevation_file="b3d_pt45_802yrs_high-elevations.csv",
                dune_file="pathways-dunes.npy",
                overwash_filter=90,  # corresponds with commercial
                overwash_to_dune=9,
                nourishment_volume=100,  # m^3/m
                beach_width_threshold=30,  # m
                background_erosion=0.0,
                rebuild_dune_threshold=1,
            )

            cascade_pt75_h2m_high_nourishment_commercial = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                nt=10,
                rmin=0.55,
                rmax=0.95,  # rave = 0.75
                name="8-B3D_Rave_pt75_Nourishment_2mDune_highEle_commercial",
                dune_design_elevation=4.1,  # m MHW, keep dune design height the same as 2 m dune above the "roadway"
                storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                elevation_file="b3d_pt75_829yrs_high-elevations.csv",
                dune_file="pathways-dunes.npy",
                overwash_filter=90,  # corresponds with commercial
                overwash_to_dune=9,
                nourishment_volume=100,  # m^3/m
                beach_width_threshold=30,  # m
                background_erosion=0.0,
                rebuild_dune_threshold=1,
            )

        def old_versions():

            # note, we keep all other variables the same for comparison to the roadways scenarios, except here, we test
            # the sensitivity of the dune rebuilding threshold: 1) only rebuild if it is totally wiped out (we specify 0.3 m
            # above the berm) or 2) rebuild if the dune is eroded to 1-m above the berm
            def rebuild_threshold_pt3m():
                # Roadway scenario drowned at 162 years
                # Community reached minimum width, drowned at 178 years
                cascade_pt75_h2m_low_nourishment_residential_RTpt3m = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                    nt=1000,
                    rmin=0.55,
                    rmax=0.95,  # rave = 0.75
                    name="8-B3D_Rave_pt75_Nourishment_2mDune_lowEle_residential_rebuildpt3m",
                    dune_design_elevation=3.2,
                    # m MHW, keep dune design height the same as 2m dune above the initial "roadway"
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt75_3284yrs_low-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    overwash_filter=40,  # corresponds with residential
                    overwash_to_dune=9,
                    nourishment_volume=100,  # m^3/m
                    beach_width_threshold=30,  # m
                    background_erosion=0.0,
                    rebuild_dune_threshold=0.3,  # m above the berm elevation
                )

                # Community reached minimum width, drowned at 80 years
                cascade_pt75_h2m_low_nourishment_commercial_RTpt3m = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                    nt=1000,
                    rmin=0.55,
                    rmax=0.95,  # rave = 0.75
                    name="8-B3D_Rave_pt75_Nourishment_2mDune_lowEle_commercial_rebuildpt3m",
                    dune_design_elevation=3.2,
                    # m MHW, keep dune design height the same as 2 m dune above the "roadway"
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt75_3284yrs_low-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    overwash_filter=90,  # corresponds with commercial
                    overwash_to_dune=9,
                    nourishment_volume=100,  # m^3/m
                    beach_width_threshold=30,  # m
                    background_erosion=0.0,
                    rebuild_dune_threshold=0.3,  # m above the berm elevation
                )

                # Community reached minimum width, drowned at 80 years
                cascade_pt75_h2m_low_nourishment_commercial_BE1m_RTpt3m = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                    nt=1000,
                    rmin=0.55,
                    rmax=0.95,  # rave = 0.75
                    name="8-B3D_Rave_pt75_Nourishment_2mDune_lowEle_commercial_backerosion1m_rebuildpt3m",
                    dune_design_elevation=3.2,
                    # m MHW, keep dune design height the same as 2 m dune above the "roadway"
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt75_3284yrs_low-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    overwash_filter=90,  # corresponds with commercial
                    overwash_to_dune=9,
                    nourishment_volume=100,  # m^3/m
                    beach_width_threshold=30,  # m
                    background_erosion=-1.0,  # m/yr, background shoreline erosion
                    rebuild_dune_threshold=0.3,  # m above the berm elevation
                )

                # Roadway scenario drowned at 404 years
                # Community reached minimum width, drowned at 648 years, barrier HEIGHT DROWNED at t = 710 years
                cascade_pt45_h2m_high_nourishment_residential_RTpt3m = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                    nt=1000,
                    rmin=0.25,
                    rmax=0.65,  # rave = 0.45
                    name="8-B3D_Rave_pt45_Nourishment_2mDune_highEle_residential_rebuildpt3m",
                    dune_design_elevation=3.7,
                    # m MHW, keep dune design height the same as 2 m dune above the "roadway"
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt45_802yrs_high-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    overwash_filter=40,
                    overwash_to_dune=9,
                    nourishment_volume=100,  # m^3/m
                    beach_width_threshold=30,  # m
                    background_erosion=0.0,
                    rebuild_dune_threshold=0.3,  # m above the berm elevation
                )

                # Community reached minimum width, drowned at 426 years; Barrier has HEIGHT DROWNED at t = 452 years
                cascade_pt45_h2m_high_nourishment_commercial_RTpt3m = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                    nt=1000,
                    rmin=0.25,
                    rmax=0.65,  # rave = 0.45
                    name="8-B3D_Rave_pt45_Nourishment_2mDune_highEle_commercial_rebuildpt3m",
                    dune_design_elevation=3.7,
                    # m MHW, keep dune design height the same as 2 m dune above the "roadway"
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt45_802yrs_high-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    overwash_filter=90,  # corresponds with commercial
                    overwash_to_dune=9,
                    nourishment_volume=100,  # m^3/m
                    beach_width_threshold=30,  # m
                    background_erosion=0.0,
                    rebuild_dune_threshold=0.3,  # m above the berm elevation
                )

                # # Community reached minimum width, drowned at 426 years
                # cascade_pt45_h2m_high_nourishment_commercial_BEpt25m_RTpt3m = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                #     nt=1000,
                #     rmin=0.25,
                #     rmax=0.65,  # rave = 0.45
                #     name="8-B3D_Rave_pt45_Nourishment_2mDune_highEle_commercial_backerosionpt25m_rebuildpt3m",
                #     dune_design_elevation=3.7,  # m MHW, keep dune design height the same as 2 m dune above the "roadway"
                #     storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                #     elevation_file="b3d_pt45_802yrs_high-elevations.csv",
                #     dune_file="pathways-dunes.npy",
                #     overwash_filter=90,  # corresponds with commercial
                #     overwash_to_dune=9,
                #     nourishment_volume=100,  # m^3/m
                #     beach_width_threshold=30,  # m
                #     background_erosion=-0.25,  # m/yr, background shoreline erosion
                #     rebuild_dune_threshold=0.3,  # m above the berm elevation
                # )

                # Community reached minimum width, drowned at 426 years
                cascade_pt45_h2m_high_nourishment_commercial_BE1m_RTpt3m = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                    nt=1000,
                    rmin=0.25,
                    rmax=0.65,  # rave = 0.45
                    name="8-B3D_Rave_pt45_Nourishment_2mDune_highEle_commercial_backerosion1m_rebuildpt3m",
                    dune_design_elevation=3.7,
                    # m MHW, keep dune design height the same as 2 m dune above the "roadway"
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    elevation_file="b3d_pt45_802yrs_high-elevations.csv",
                    dune_file="pathways-dunes.npy",
                    overwash_filter=90,  # corresponds with commercial
                    overwash_to_dune=9,
                    nourishment_volume=100,  # m^3/m
                    beach_width_threshold=30,  # m
                    background_erosion=-1.0,  # m/yr, background shoreline erosion
                    rebuild_dune_threshold=0.3,  # m above the berm elevation
                )

                def old():
                    # roadway scenario drowned at 404 years
                    # Community reached minimum width, drowned at 496 years
                    cascade_pt45_h2m_low_nourishment_residential = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                        nt=500,
                        rmin=0.25,
                        rmax=0.65,  # rave = 0.45
                        name="8-B3D_Rave_pt45_Nourishment_2mDune_lowEle_residential",
                        dune_design_elevation=3.7,
                        # m MHW, keep dune design height the same as 2 m dune above the "roadway"
                        storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                        elevation_file="b3d_pt45_8750yrs_low-elevations.csv",
                        dune_file="pathways-dunes.npy",
                        overwash_filter=40,  # corresponds with commercial
                        nourishment_volume=100,  # m^3/m
                        beach_width_threshold=30,  # m
                        background_erosion=0.0,
                    )

                    # Community reached minimum width, drowned at 421 years
                    # Barrier has HEIGHT DROWNED at t = 458 years
                    cascade_pt45_h2m_low_nourishment_commercial = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                        nt=500,
                        rmin=0.25,
                        rmax=0.65,  # rave = 0.45
                        name="8-B3D_Rave_pt45_Nourishment_2mDune_lowEle_commercial",
                        dune_design_elevation=3.7,
                        # m MHW, keep dune design height the same as 2 m dune above the "roadway"
                        storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                        elevation_file="b3d_pt45_8750yrs_low-elevations.csv",
                        dune_file="pathways-dunes.npy",
                        overwash_filter=90,  # corresponds with commercial
                        nourishment_volume=100,  # m^3/m
                        beach_width_threshold=30,  # m
                        background_erosion=0.0,
                    )

                    # Community reached minimum width, drowned at 421 years
                    # Barrier has HEIGHT DROWNED at t = 454 years
                    cascade_pt45_h2m_low_nourishment_commercial_background_erosion_pt25m = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                        nt=500,
                        rmin=0.25,
                        rmax=0.65,  # rave = 0.45
                        name="8-B3D_Rave_pt45_Nourishment_2mDune_lowEle_commercial_backerosion_pt25m",
                        dune_design_elevation=3.7,
                        # m MHW, keep dune design height the same as 2 m dune above the "roadway"
                        storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                        elevation_file="b3d_pt45_8750yrs_low-elevations.csv",
                        dune_file="pathways-dunes.npy",
                        overwash_filter=90,  # corresponds with commercial
                        nourishment_volume=100,  # m^3/m
                        beach_width_threshold=30,  # m
                        background_erosion=-0.25,  # m/yr, background shoreline erosion
                    )

                    # Community reached minimum width, drowned at 421 years
                    cascade_pt45_h2m_low_nourishment_commercial_background_erosion_1m = RUN_8_CASCADE_noAST_Rave_SLR_pt004_Nourishment(
                        nt=500,
                        rmin=0.25,
                        rmax=0.65,  # rave = 0.45
                        name="8-B3D_Rave_pt45_Nourishment_2mDune_lowEle_commercial_backerosion_1m",
                        dune_design_elevation=3.7,
                        # m MHW, keep dune design height the same as 2 m dune above the "roadway"
                        storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                        elevation_file="b3d_pt45_8750yrs_low-elevations.csv",
                        dune_file="pathways-dunes.npy",
                        overwash_filter=90,  # corresponds with commercial
                        nourishment_volume=100,  # m^3/m
                        beach_width_threshold=30,  # m
                        background_erosion=-1.0,  # m/yr, background shoreline erosion
                    )

def alongshore_variable_management():
        def old_runs():
            def nourishment_pt75_low():
                # these initial conditions drowned at 80 years in nourishments
                number_barrier3d_models = 6
                beach_width_threshold = [30] * number_barrier3d_models
                rmin = [0.55] * number_barrier3d_models
                rmax = [0.95] * number_barrier3d_models
                elevation_file = [
                    "b3d_pt75_3284yrs_low-elevations.csv"
                ] * number_barrier3d_models
                dune_file = ["pathways-dunes.npy"] * number_barrier3d_models
                dune_design_elevation = [3.2] * number_barrier3d_models
                roads_on = [False] * number_barrier3d_models
                nourishments_on = [True] * number_barrier3d_models

                # all B3D segments drown at 80
                nourishment_only_6AST_low_pt75_comm_BE1m_RT1m = RUN_9_CASCADE_Rave_SLR_pt004_AlongshoreVariableManagement(
                    nt=100,
                    name="9-CASCADE_Rave_pt75_Nourishment_2mDune_lowEle_comm_BE1m_RT1m_6AST",
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    alongshore_section_count=number_barrier3d_models,  # NOTE: will want to go back to sensitivity modeling
                    num_cores=6,  # for my laptop, max is ?
                    beach_width_threshold=beach_width_threshold,  # m
                    rmin=rmin,
                    rmax=rmax,  # rave = 0.75
                    elevation_file=elevation_file,
                    dune_file=dune_file,
                    dune_design_elevation=dune_design_elevation,
                    dune_minimum_elevation=None,
                    road_ele=None,
                    road_width=None,
                    road_setback=None,
                    overwash_filter=90,  # corresponds with commercial
                    overwash_to_dune=9,
                    nourishment_volume=100,  # m^3/m
                    background_erosion=-1.00,  # m/yr, background shoreline erosion
                    rebuild_dune_threshold=1,  # m above the berm elevation
                    roadway_management_on=roads_on,
                    beach_dune_manager_on=nourishments_on,
                )

            def nourishment_pt45_high_RT1m():
                number_barrier3d_models = 6
                beach_width_threshold = [30] * number_barrier3d_models
                rmin = [0.25] * number_barrier3d_models
                rmax = [0.65] * number_barrier3d_models
                elevation_file = [
                    "b3d_pt45_802yrs_high-elevations.csv"
                ] * number_barrier3d_models
                dune_file = ["pathways-dunes.npy"] * number_barrier3d_models
                dune_design_elevation = [3.2] * number_barrier3d_models
                roads_on = [False] * number_barrier3d_models
                nourishments_on = [True] * number_barrier3d_models

                nourishment_only_6AST_low_pt75_comm_BE1m_RT1m = RUN_9_CASCADE_Rave_SLR_pt004_AlongshoreVariableManagement(
                    nt=100,
                    name="9-CASCADE_Rave_pt45_Nourishment_2mDune_highEle_res_BE1m_RT1m_6AST",
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    alongshore_section_count=number_barrier3d_models,  # NOTE: will want to go back to sensitivity modeling
                    num_cores=6,  # for my laptop, max is ?
                    beach_width_threshold=beach_width_threshold,  # m
                    rmin=rmin,
                    rmax=rmax,  # rave = 0.45
                    elevation_file=elevation_file,
                    dune_file=dune_file,
                    dune_design_elevation=dune_design_elevation,
                    dune_minimum_elevation=None,
                    road_ele=None,
                    road_width=None,
                    road_setback=None,
                    overwash_filter=90,  # corresponds with commercial
                    overwash_to_dune=9,
                    nourishment_volume=100,  # m^3/m
                    background_erosion=-1.00,  # m/yr, background shoreline erosion
                    rebuild_dune_threshold=1,  # m above the berm elevation, more realistic is 1 m
                    roadway_management_on=roads_on,
                    beach_dune_manager_on=nourishments_on,
                )

            def nourishment_pt45_high_RTpt3m():
                # nourishments only community drowned at 426 years; Barrier has HEIGHT DROWNED at t = 452 years
                number_barrier3d_models = 6
                beach_width_threshold = [30] * number_barrier3d_models
                rmin = [0.25] * number_barrier3d_models
                rmax = [0.65] * number_barrier3d_models
                elevation_file = [
                    "b3d_pt45_802yrs_high-elevations.csv"
                ] * number_barrier3d_models
                dune_file = ["pathways-dunes.npy"] * number_barrier3d_models
                dune_design_elevation = [3.2] * number_barrier3d_models
                roads_on = [False] * number_barrier3d_models
                nourishments_on = [True] * number_barrier3d_models

                # Community reached minimum width, drowned at 485 years
                nourishment_only_6AST_low_pt75_comm_BE1m_RT1m = RUN_9_CASCADE_Rave_SLR_pt004_AlongshoreVariableManagement(
                    nt=500,
                    name="9-CASCADE_Rave_pt45_Nourishment_2mDune_highEle_res_BE1m_RT1m_6AST",
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    alongshore_section_count=number_barrier3d_models,  # NOTE: will want to go back to sensitivity modeling
                    num_cores=6,  # for my laptop, max is ?
                    beach_width_threshold=beach_width_threshold,  # m
                    rmin=rmin,
                    rmax=rmax,  # rave = 0.45
                    elevation_file=elevation_file,
                    dune_file=dune_file,
                    dune_design_elevation=dune_design_elevation,
                    dune_minimum_elevation=None,
                    road_ele=None,
                    road_width=None,
                    road_setback=None,
                    overwash_filter=90,  # corresponds with commercial
                    overwash_to_dune=9,
                    nourishment_volume=100,  # m^3/m
                    background_erosion=0,  # m/yr, background shoreline erosion
                    rebuild_dune_threshold=0.3,  # m above the berm elevation
                    roadway_management_on=roads_on,
                    beach_dune_manager_on=nourishments_on,
                )

            def nourishment_pt75_low_split_natural():
                # these initial conditions drowned at 80 years in nourishments
                number_barrier3d_models = 6
                beach_width_threshold = [30] * number_barrier3d_models
                rmin = [0.55] * number_barrier3d_models
                rmax = [0.95] * number_barrier3d_models
                elevation_file = [
                    "b3d_pt75_3284yrs_low-elevations.csv"
                ] * number_barrier3d_models
                dune_file = ["pathways-dunes.npy"] * number_barrier3d_models
                dune_design_elevation = [3.2] * number_barrier3d_models
                roads_on = [False] * number_barrier3d_models
                nourishments_on = [True, True, True, False, False, False]

                # very quickly these barriers separate -- MAKES SENSE, but not interesting to show
                nourish_natural_6AST_low_pt75_comm_BE1m_RT1m = RUN_9_CASCADE_Rave_SLR_pt004_AlongshoreVariableManagement(
                    nt=100,
                    name="9-CASCADE_Rave_pt75_2mDune_lowEle_comm_BE1m_RT1m_6AST_nourish_nat",
                    storm_file="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy",
                    alongshore_section_count=number_barrier3d_models,  # NOTE: will want to go back to sensitivity modeling
                    num_cores=6,  # for my laptop, max is ?
                    beach_width_threshold=beach_width_threshold,  # m
                    rmin=rmin,
                    rmax=rmax,  # rave = 0.75
                    elevation_file=elevation_file,
                    dune_file=dune_file,
                    dune_design_elevation=dune_design_elevation,
                    dune_minimum_elevation=None,
                    road_ele=None,
                    road_width=None,
                    road_setback=None,
                    overwash_filter=90,  # corresponds with commercial
                    overwash_to_dune=9,
                    nourishment_volume=100,  # m^3/m
                    background_erosion=-1.00,  # m/yr, background shoreline erosion
                    rebuild_dune_threshold=1,  # m above the berm elevation
                    roadway_management_on=roads_on,
                    beach_dune_manager_on=nourishments_on,
                )

        def nourishment_pt75_low_split_roadways_BE1m_3km():

            # variables that DO NOT change among runs
            number_barrier3d_models = 6
            beach_width_threshold = [30] * number_barrier3d_models
            rmin = [0.55] * number_barrier3d_models
            rmax = [0.95] * number_barrier3d_models
            elevation_file = [
                "b3d_pt75_4261yrs_low-elevations.csv"
            ] * number_barrier3d_models
            dune_file = ["pathways-dunes.npy"] * number_barrier3d_models
            storm_file = "StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy"
            dune_design_elevation = [2.6] * number_barrier3d_models  # 2 m scenario
            num_cores = 6  # for my laptop, max is 15
            dune_minimum_elevation = 1.1  # m MHW, allow dune to erode down to 0.5 m above the roadway, for roadways only
            road_ele = 0.6  # m MHW
            road_width = 20  # m
            road_setback = 20  # m
            overwash_filter = 90  # commercial
            overwash_to_dune = 9
            nourishment_volume = 100  # m^3/m
            background_erosion = -1.0  # m/yr, background shoreline erosion
            rebuild_dune_threshold = 1  # m

            # baseline models for comparison -- all roadways ----------------------------------------
            roads_on = [True, True, True, True, True, True]
            nourishments_on = [False, False, False, False, False, False]
            sea_level_rise_rate = 0.004
            sea_level_constant = True  # linear

            # Island is too narrow for roadway to be relocated. Roadway eaten up by dunes at 73 years
            roadways_6AST_low_pt75_BE1m = (
                RUN_9_CASCADE_Rave_SLR_pt004_AlongshoreVariableManagement(
                    nt=200,
                    name="9-CASCADE_Rave_pt75_2mDune_lowEle_BE1m_6AST_6roads",
                    storm_file=storm_file,
                    alongshore_section_count=number_barrier3d_models,
                    num_cores=num_cores,
                    beach_width_threshold=beach_width_threshold,
                    rmin=rmin,
                    rmax=rmax,  # rave = 0.75
                    elevation_file=elevation_file,
                    dune_file=dune_file,
                    dune_design_elevation=dune_design_elevation,
                    dune_minimum_elevation=dune_minimum_elevation,
                    road_ele=road_ele,
                    road_width=road_width,
                    road_setback=road_setback,
                    overwash_filter=overwash_filter,
                    overwash_to_dune=overwash_to_dune,
                    nourishment_volume=nourishment_volume,
                    background_erosion=background_erosion,
                    rebuild_dune_threshold=rebuild_dune_threshold,
                    roadway_management_on=roads_on,
                    beach_dune_manager_on=nourishments_on,
                    sea_level_rise_rate=sea_level_rise_rate,
                    sea_level_constant=sea_level_constant,
                )
            )

            # baseline models for comparison -- all nourishments ----------------------------------------
            roads_on = [False, False, False, False, False, False]
            nourishments_on = [True, True, True, True, True, True]
            sea_level_rise_rate = 0.004
            sea_level_constant = True  # linear

            # Community reached minimum width, drowned at 83 years
            community_6AST_low_pt75_BE1m = RUN_9_CASCADE_Rave_SLR_pt004_AlongshoreVariableManagement(
                nt=200,
                name="9-CASCADE_Rave_pt75_2mDune_lowEle_comm_BE1m_RT1m_6AST_6nourish",
                storm_file=storm_file,
                alongshore_section_count=number_barrier3d_models,
                num_cores=num_cores,
                beach_width_threshold=beach_width_threshold,
                rmin=rmin,
                rmax=rmax,  # rave = 0.75
                elevation_file=elevation_file,
                dune_file=dune_file,
                dune_design_elevation=dune_design_elevation,
                dune_minimum_elevation=dune_minimum_elevation,
                road_ele=road_ele,
                road_width=road_width,
                road_setback=road_setback,
                overwash_filter=overwash_filter,
                overwash_to_dune=overwash_to_dune,
                nourishment_volume=nourishment_volume,
                background_erosion=background_erosion,
                rebuild_dune_threshold=rebuild_dune_threshold,
                roadway_management_on=roads_on,
                beach_dune_manager_on=nourishments_on,
                sea_level_rise_rate=sea_level_rise_rate,
                sea_level_constant=sea_level_constant,
            )

            # split management - 1 m background erosion and 0.004 m/yr SLR ----------------------------------------
            roads_on = [False, False, False, True, True, True]
            nourishments_on = [True, True, True, False, False, False]
            sea_level_rise_rate = 0.004
            sea_level_constant = True  # linear

            # All 3: Community reached minimum width, drowned at 83 years
            # All 3: Island is too narrow for roadway to be relocated. Roadway eaten up by dunes at 143 years
            nourishment_roadways_6AST_low_pt75_comm_BE1m_RT1m = RUN_9_CASCADE_Rave_SLR_pt004_AlongshoreVariableManagement(
                nt=200,
                name="9-CASCADE_Rave_pt75_Nourish_2mDune_lowEle_comm_BE1m_RT1m_6AST_3roads",
                storm_file=storm_file,
                alongshore_section_count=number_barrier3d_models,
                num_cores=num_cores,
                beach_width_threshold=beach_width_threshold,
                rmin=rmin,
                rmax=rmax,  # rave = 0.75
                elevation_file=elevation_file,
                dune_file=dune_file,
                dune_design_elevation=dune_design_elevation,
                dune_minimum_elevation=dune_minimum_elevation,
                road_ele=road_ele,
                road_width=road_width,
                road_setback=road_setback,
                overwash_filter=overwash_filter,
                overwash_to_dune=overwash_to_dune,
                nourishment_volume=nourishment_volume,
                background_erosion=background_erosion,
                rebuild_dune_threshold=rebuild_dune_threshold,
                roadway_management_on=roads_on,
                beach_dune_manager_on=nourishments_on,
                sea_level_rise_rate=sea_level_rise_rate,
                sea_level_constant=sea_level_constant,
            )

            # split management - 1 m background erosion and accelerated SLR ----------------------------------------
            roads_on = [False, False, False, True, True, True]
            nourishments_on = [True, True, True, False, False, False]
            sea_level_rise_rate = 0.004  # dummy here
            sea_level_constant = False  # accelerated

            # All 3: Community reached minimum width, drowned at 64 years
            # All 3: Barrier has HEIGHT DROWNED at t = 85 years
            nourishment_roadways_6AST_low_pt75_comm_BE1m_RT1m = RUN_9_CASCADE_Rave_SLR_pt004_AlongshoreVariableManagement(
                nt=200,
                name="9-CASCADE_Rave_pt75_Nourish_2mDune_lowEle_comm_BE1m_RT1m_6AST_3roads_AccSLR",
                storm_file=storm_file,
                alongshore_section_count=number_barrier3d_models,
                num_cores=num_cores,
                beach_width_threshold=beach_width_threshold,
                rmin=rmin,
                rmax=rmax,  # rave = 0.75
                elevation_file=elevation_file,
                dune_file=dune_file,
                dune_design_elevation=dune_design_elevation,
                dune_minimum_elevation=dune_minimum_elevation,
                road_ele=road_ele,
                road_width=road_width,
                road_setback=road_setback,
                overwash_filter=overwash_filter,
                overwash_to_dune=overwash_to_dune,
                nourishment_volume=nourishment_volume,
                background_erosion=background_erosion,
                rebuild_dune_threshold=rebuild_dune_threshold,
                roadway_management_on=roads_on,
                beach_dune_manager_on=nourishments_on,
                sea_level_rise_rate=sea_level_rise_rate,
                sea_level_constant=sea_level_constant,
            )

        def nourishment_pt45_low_left_roadways_pt75_low_right_BE1m_3km():

            # variables that DO NOT change among runs
            number_barrier3d_models = 6
            beach_width_threshold = [30] * number_barrier3d_models
            rmin = [0.25] * 3 + [0.55] * 3
            rmax = [0.65] * 3 + [0.95] * 3
            elevation_file = ["b3d_pt45_8757yrs_low-elevations.csv"] * 3 + [
                "b3d_pt75_4261yrs_low-elevations.csv"
            ] * 3
            dune_file = ["pathways-dunes.npy"] * number_barrier3d_models
            storm_file = "StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy"
            dune_design_elevation = [3.6] * 3 + [2.6] * 3  # 2 m above the roadway
            dune_minimum_elevation = [2.1] * 3 + [
                1.1
            ] * 3  # m MHW, allow dune to erode down to 0.5 m above the roadway, for roadways only (others dummy)
            road_ele = [1.6] * 3 + [
                0.6
            ] * 3  # first 3 are dummys since we are only doing nourishment there
            num_cores = 6  # for my laptop, max is 15
            road_width = 20  # m
            road_setback = 20  # m
            overwash_filter = 90  # commercial
            overwash_to_dune = 9
            nourishment_volume = 100  # m^3/m
            background_erosion = -1.0  # m/yr, background shoreline erosion
            rebuild_dune_threshold = 1  # m, for nourishments only

            # split management - 1 m background erosion and 0.004 m/yr SLR ----------------------------------------
            roads_on = [False, False, False, True, True, True]
            nourishments_on = [True, True, True, False, False, False]
            sea_level_rise_rate = 0.004
            sea_level_constant = True  # linear

            # All 3: Roadway drowned in place at 132 years due to SLR - road cannot be below 0 m MHW
            nourishment_roadways_6AST_low_pt45_pt75_comm_BE1m_RT1m = RUN_9_CASCADE_Rave_SLR_pt004_AlongshoreVariableManagement(
                nt=200,
                name="9-CASCADE_Rave_pt45_pt75_low_split_2mDune_comm_BE1m_RT1m_6AST_3roads",
                storm_file=storm_file,
                alongshore_section_count=number_barrier3d_models,
                num_cores=num_cores,
                beach_width_threshold=beach_width_threshold,
                rmin=rmin,
                rmax=rmax,
                elevation_file=elevation_file,
                dune_file=dune_file,
                dune_design_elevation=dune_design_elevation,
                dune_minimum_elevation=dune_minimum_elevation,
                road_ele=road_ele,
                road_width=road_width,
                road_setback=road_setback,
                overwash_filter=overwash_filter,
                overwash_to_dune=overwash_to_dune,
                nourishment_volume=nourishment_volume,
                background_erosion=background_erosion,
                rebuild_dune_threshold=rebuild_dune_threshold,
                roadway_management_on=roads_on,
                beach_dune_manager_on=nourishments_on,
                sea_level_rise_rate=sea_level_rise_rate,
                sea_level_constant=sea_level_constant,
            )

            # split management - add accelerated SLR ----------------------------------------
            roads_on = [False, False, False, True, True, True]
            nourishments_on = [True, True, True, False, False, False]
            sea_level_rise_rate = 0.004  # dummy here
            sea_level_constant = False  # accelerated

            # All three: Roadway drowned in place at 85 years due to SLR - road cannot be below 0 m MHW
            # All three: Community reached minimum width, drowned at 137 years
            # Barrier has HEIGHT DROWNED at t = 141 years
            nourishment_roadways_6AST_low_pt75_comm_BE1m_RT1m = RUN_9_CASCADE_Rave_SLR_pt004_AlongshoreVariableManagement(
                nt=200,
                name="9-CASCADE_Rave_pt45_pt75_low_split_2mDune_comm_BE1m_RT1m_6AST_3roads_AccSLR",
                storm_file=storm_file,
                alongshore_section_count=number_barrier3d_models,
                num_cores=num_cores,
                beach_width_threshold=beach_width_threshold,
                rmin=rmin,
                rmax=rmax,
                elevation_file=elevation_file,
                dune_file=dune_file,
                dune_design_elevation=dune_design_elevation,
                dune_minimum_elevation=dune_minimum_elevation,
                road_ele=road_ele,
                road_width=road_width,
                road_setback=road_setback,
                overwash_filter=overwash_filter,
                overwash_to_dune=overwash_to_dune,
                nourishment_volume=nourishment_volume,
                background_erosion=background_erosion,
                rebuild_dune_threshold=rebuild_dune_threshold,
                roadway_management_on=roads_on,
                beach_dune_manager_on=nourishments_on,
                sea_level_rise_rate=sea_level_rise_rate,
                sea_level_constant=sea_level_constant,
            )

            # baseline pt45 low -- all nourishment ----------------------------------------
            number_barrier3d_models = 6
            beach_width_threshold = [30] * number_barrier3d_models
            rmin = [0.25] * number_barrier3d_models
            rmax = [0.65] * number_barrier3d_models
            elevation_file = [
                "b3d_pt45_8757yrs_low-elevations.csv"
            ] * number_barrier3d_models
            dune_file = ["pathways-dunes.npy"] * number_barrier3d_models
            storm_file = "StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy"
            dune_design_elevation = [
                3.6
            ] * number_barrier3d_models  # 2 m above the roadway
            dune_minimum_elevation = [2.1] * number_barrier3d_models  # dummy
            road_ele = [1.6] * number_barrier3d_models  # dummy
            num_cores = 6  # for my laptop, max is 15
            road_width = 20  # m, dummy
            road_setback = 20  # m, dummy
            overwash_filter = 90  # commercial
            overwash_to_dune = 9
            nourishment_volume = 100  # m^3/m
            background_erosion = -1.0  # m/yr, background shoreline erosion
            rebuild_dune_threshold = 1  # m, for nourishments only

            roads_on = [False, False, False, False, False, False]
            nourishments_on = [True, True, True, True, True, True]
            sea_level_rise_rate = 0.004
            sea_level_constant = True  # linear

            nourishment_6AST_low_pt45_comm_BE1m_RT1m = RUN_9_CASCADE_Rave_SLR_pt004_AlongshoreVariableManagement(
                nt=200,
                name="9-CASCADE_Rave_pt45_low_nourishment_2mDune_comm_BE1m_RT1m_6AST",
                storm_file=storm_file,
                alongshore_section_count=number_barrier3d_models,
                num_cores=num_cores,
                beach_width_threshold=beach_width_threshold,
                rmin=rmin,
                rmax=rmax,
                elevation_file=elevation_file,
                dune_file=dune_file,
                dune_design_elevation=dune_design_elevation,
                dune_minimum_elevation=dune_minimum_elevation,
                road_ele=road_ele,
                road_width=road_width,
                road_setback=road_setback,
                overwash_filter=overwash_filter,
                overwash_to_dune=overwash_to_dune,
                nourishment_volume=nourishment_volume,
                background_erosion=background_erosion,
                rebuild_dune_threshold=rebuild_dune_threshold,
                roadway_management_on=roads_on,
                beach_dune_manager_on=nourishments_on,
                sea_level_rise_rate=sea_level_rise_rate,
                sea_level_constant=sea_level_constant,
            )

        def nourishment_pt45_low_left_middle_pt75_low_roadways_right_pt45_low_roadways_4pt5km():
            # this new run: better illustrates what abandoning in the middle of a domain looks like (Rodanthe)
            # --- natural dune dynamics don't really matter here b/s we are managing all of them ---
            # left: low but wide barrier -- nourishments (pt45 low)
            # middle: low but narrow barrier -- roadways (pt75 low)
            # right: low but wide barrier -- roadways (pt45 low)

            # variables that DO NOT change among runs
            # (NOTE: these variables the same as above -- we maintain a 2 m dune)
            number_barrier3d_models = 9
            beach_width_threshold = [30] * number_barrier3d_models
            rmin = [0.25] * 3 + [0.55] * 3 + [0.25] * 3
            rmax = [0.65] * 3 + [0.95] * 3 + [0.65] * 3
            elevation_file = (
                ["b3d_pt45_8757yrs_low-elevations.csv"] * 3
                + ["b3d_pt75_4261yrs_low-elevations.csv"] * 3
                + ["b3d_pt45_8757yrs_low-elevations.csv"] * 3
            )
            dune_file = ["pathways-dunes.npy"] * number_barrier3d_models
            storm_file = "StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_01.npy"
            dune_design_elevation = (
                [3.6] * 3 + [2.6] * 3 + [3.6] * 3
            )  # 2 m above the original roadway
            dune_minimum_elevation = (
                [2.1] * 3 + [1.1] * 3 + [2.1] * 3
            )  # m MHW, allow dune to erode down to 0.5 m above the roadway, roadways only (others dummy)
            road_ele = (
                [1.6] * 3 + [0.6] * 3 + [1.6] * 3
            )  # first 3 are dummys since we are only doing nourishment there
            num_cores = 9  # for my laptop, max is 15
            road_width = 20  # m
            road_setback = 20  # m
            overwash_filter = 90  # commercial
            overwash_to_dune = 9
            nourishment_volume = 100  # m^3/m
            background_erosion = -1.0  # m/yr, background shoreline erosion
            rebuild_dune_threshold = 1  # m
            roads_on = [False, False, False, True, True, True, True, True, True]
            nourishments_on = [
                True,
                True,
                True,
                False,
                False,
                False,
                False,
                False,
                False,
            ]

            # 1 m background erosion and 0.004 m/yr SLR ----------------------------------------
            sea_level_rise_rate = 0.004
            sea_level_constant = True  # linear

            # 1353 config, Barrier has HEIGHT DROWNED at t = 132
            # 6490 config, Barrier has HEIGHT DROWNED at t = 147 years
            # 3284 config is wider and higher (190 m wide vs. 144 m for 4261): no roadway drowned
            # *** 4261, Roadway drowned at 99, 115, 131 due to SLR, road cannot be below 0 m MHW -- created curved shape
            # After I grouped roadway abandonment, all three in the middle are abandoned at 99 years
            AST_3domains_BE1m = RUN_9_CASCADE_Rave_SLR_pt004_AlongshoreVariableManagement(
                nt=200,
                name="9-CASCADE_AST_3domains_BE1m",
                storm_file=storm_file,
                alongshore_section_count=number_barrier3d_models,
                num_cores=num_cores,
                beach_width_threshold=beach_width_threshold,
                rmin=rmin,
                rmax=rmax,
                elevation_file=elevation_file,
                dune_file=dune_file,
                dune_design_elevation=dune_design_elevation,
                dune_minimum_elevation=dune_minimum_elevation,
                road_ele=road_ele,
                road_width=road_width,
                road_setback=road_setback,
                trigger_dune_knockdown=False,  # this didn't really do anything due to the timing of storms
                group_roadway_abandonment=[0, 0, 0, 1, 1, 1, 2, 2, 2],
                overwash_filter=overwash_filter,
                overwash_to_dune=overwash_to_dune,
                nourishment_volume=nourishment_volume,
                background_erosion=background_erosion,
                rebuild_dune_threshold=rebuild_dune_threshold,
                roadway_management_on=roads_on,
                beach_dune_manager_on=nourishments_on,
                sea_level_rise_rate=sea_level_rise_rate,
                sea_level_constant=sea_level_constant,
            )

            # 1 m background erosion and accelerated SLR ----------------------------------------
            sea_level_rise_rate = 0.004  # dummy
            sea_level_constant = False  # accelerated

            # Barrier has HEIGHT DROWNED at t = 71 years (#5 B3D) - 4261
            # even if I change the dune design height to <1 m, this barrier wants to drown due to Acc SLR
            AST_3domains_AccSLR_BE1m = (
                RUN_9_CASCADE_Rave_SLR_pt004_AlongshoreVariableManagement(
                    nt=200,
                    name="9-CASCADE_AST_3domains_BE1m_AccSLR",
                    storm_file=storm_file,
                    alongshore_section_count=number_barrier3d_models,
                    num_cores=num_cores,
                    beach_width_threshold=beach_width_threshold,
                    rmin=rmin,
                    rmax=rmax,
                    elevation_file=elevation_file,
                    dune_file=dune_file,
                    dune_design_elevation=dune_design_elevation,
                    dune_minimum_elevation=dune_minimum_elevation,
                    road_ele=road_ele,
                    road_width=road_width,
                    road_setback=road_setback,
                    group_roadway_abandonment=[0, 0, 0, 1, 1, 1, 2, 2, 2],
                    overwash_filter=overwash_filter,
                    overwash_to_dune=overwash_to_dune,
                    nourishment_volume=nourishment_volume,
                    background_erosion=background_erosion,
                    rebuild_dune_threshold=rebuild_dune_threshold,
                    roadway_management_on=roads_on,
                    beach_dune_manager_on=nourishments_on,
                    sea_level_rise_rate=sea_level_rise_rate,
                    sea_level_constant=sea_level_constant,
                )
            )

            # NO background erosion and accelerated SLR (just talk about this one) ----------------------------
            sea_level_rise_rate = 0.004  # dummy
            sea_level_constant = False  # accelerated
            background_erosion = 0.0

            # Barrier has HEIGHT DROWNED at t = 92 years
            AST_3domains_AccSLR = (
                RUN_9_CASCADE_Rave_SLR_pt004_AlongshoreVariableManagement(
                    nt=200,
                    name="9-CASCADE_AST_3domains_AccSLR",
                    storm_file=storm_file,
                    alongshore_section_count=number_barrier3d_models,
                    num_cores=num_cores,
                    beach_width_threshold=beach_width_threshold,
                    rmin=rmin,
                    rmax=rmax,
                    elevation_file=elevation_file,
                    dune_file=dune_file,
                    dune_design_elevation=dune_design_elevation,
                    dune_minimum_elevation=dune_minimum_elevation,
                    road_ele=road_ele,
                    road_width=road_width,
                    road_setback=road_setback,
                    group_roadway_abandonment=[0, 0, 0, 1, 1, 1, 2, 2, 2],
                    overwash_filter=overwash_filter,
                    overwash_to_dune=overwash_to_dune,
                    nourishment_volume=nourishment_volume,
                    background_erosion=background_erosion,
                    rebuild_dune_threshold=rebuild_dune_threshold,
                    roadway_management_on=roads_on,
                    beach_dune_manager_on=nourishments_on,
                    sea_level_rise_rate=sea_level_rise_rate,
                    sea_level_constant=sea_level_constant,
                )
            )

            # 1 m background erosion and accelerated SLR, middle natural scenario (adaptation scenario) ---------------
            sea_level_rise_rate = 0.004  # dummy
            sea_level_constant = False  # accelerated

            # set middle to no management and let's see what happens
            roads_on = [False, False, False, False, False, False, True, True, True]

            # Roadway width drowned at 137 years, 20.0% of road borders water
            # All: Community reached minimum width, drowned at 137 years
            # Roadway width drowned at 142 years, 20.0% of road borders water
            # Island is too narrow for roadway to be relocated. Roadway eaten up by dunes at 149 years
            # ---- With new roadway abandonment grouping, all drown at 137 (roadway and community) ----
            AST_3domains_AccSLR_BE1m = (
                RUN_9_CASCADE_Rave_SLR_pt004_AlongshoreVariableManagement(
                    nt=200,
                    name="9-CASCADE_AST_3domains_BE1m_AccSLR_nat_middle",
                    storm_file=storm_file,
                    alongshore_section_count=number_barrier3d_models,
                    num_cores=num_cores,
                    beach_width_threshold=beach_width_threshold,
                    rmin=rmin,
                    rmax=rmax,
                    elevation_file=elevation_file,
                    dune_file=dune_file,
                    dune_design_elevation=dune_design_elevation,
                    dune_minimum_elevation=dune_minimum_elevation,
                    road_ele=road_ele,
                    road_width=road_width,
                    road_setback=road_setback,
                    group_roadway_abandonment=[0, 0, 0, 0, 0, 0, 1, 1, 1],
                    overwash_filter=overwash_filter,
                    overwash_to_dune=overwash_to_dune,
                    nourishment_volume=nourishment_volume,
                    background_erosion=background_erosion,
                    rebuild_dune_threshold=rebuild_dune_threshold,
                    roadway_management_on=roads_on,
                    beach_dune_manager_on=nourishments_on,
                    sea_level_rise_rate=sea_level_rise_rate,
                    sea_level_constant=sea_level_constant,
                )
            )

        def averages():
            def one_hundred_thirds_acc_BE1m_ast_runs(
                storm_start=0,
                storm_end=100,
                name_prefix_1="9-CASCADE_AST_3domains_BE1m_AccSLR",
                name_prefix_2="9-CASCADE_AST_3domains_BE1m_AccSLR",
                storm_prefix="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_",
            ):

                # variables that DO NOT change among runs
                # (NOTE: these variables the same as above -- we maintain a 2 m dune)
                number_barrier3d_models = 9
                beach_width_threshold = [30] * number_barrier3d_models
                rmin = [0.25] * 3 + [0.55] * 3 + [0.25] * 3
                rmax = [0.65] * 3 + [0.95] * 3 + [0.65] * 3
                elevation_file = (
                    ["b3d_pt45_8757yrs_low-elevations.csv"] * 3
                    + ["b3d_pt75_4261yrs_low-elevations.csv"] * 3
                    + ["b3d_pt45_8757yrs_low-elevations.csv"] * 3
                )
                dune_file = ["pathways-dunes.npy"] * number_barrier3d_models
                dune_design_elevation = (
                    [3.6] * 3 + [2.6] * 3 + [3.6] * 3
                )  # 2 m above the original roadway
                dune_minimum_elevation = (
                    [2.1] * 3 + [1.1] * 3 + [2.1] * 3
                )  # m MHW, allow dune to erode down to 0.5 m above the roadway, roadways only (others dummy)
                road_ele = (
                    [1.6] * 3 + [0.6] * 3 + [1.6] * 3
                )  # first 3 are dummys since we are only doing nourishment there
                num_cores = 9
                road_width = 20  # m
                road_setback = 20  # m
                overwash_filter = 90  # commercial
                overwash_to_dune = 9
                nourishment_volume = 100  # m^3/m
                background_erosion = -1.0  # m/yr, background shoreline erosion
                rebuild_dune_threshold = 1  # m
                nourishments_on = [
                    True,
                    True,
                    True,
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                ]

                sea_level_rise_rate = 0.004  # dummy
                sea_level_constant = False  # accelerated

                for iStorm in range(storm_start, storm_end):
                    name = name_prefix_1 + str(iStorm)
                    storm_file = storm_prefix + str(iStorm) + ".npy"

                    roads_on = [False, False, False, True, True, True, True, True, True]

                    RUN_9_CASCADE_Rave_SLR_pt004_AlongshoreVariableManagement(
                        nt=200,
                        name=name,
                        storm_file=storm_file,
                        alongshore_section_count=number_barrier3d_models,
                        num_cores=num_cores,
                        beach_width_threshold=beach_width_threshold,
                        rmin=rmin,
                        rmax=rmax,
                        elevation_file=elevation_file,
                        dune_file=dune_file,
                        dune_design_elevation=dune_design_elevation,
                        dune_minimum_elevation=dune_minimum_elevation,
                        road_ele=road_ele,
                        road_width=road_width,
                        road_setback=road_setback,
                        group_roadway_abandonment=[0, 0, 0, 1, 1, 1, 2, 2, 2],
                        overwash_filter=overwash_filter,
                        overwash_to_dune=overwash_to_dune,
                        nourishment_volume=nourishment_volume,
                        background_erosion=background_erosion,
                        rebuild_dune_threshold=rebuild_dune_threshold,
                        roadway_management_on=roads_on,
                        beach_dune_manager_on=nourishments_on,
                        sea_level_rise_rate=sea_level_rise_rate,
                        sea_level_constant=sea_level_constant,
                    )

                    # set middle to no management and lets see what happens
                    roads_on = [
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        True,
                        True,
                        True,
                    ]

                    name = name_prefix_2 + str(iStorm)

                    RUN_9_CASCADE_Rave_SLR_pt004_AlongshoreVariableManagement(
                        nt=200,
                        name=name,
                        storm_file=storm_file,
                        alongshore_section_count=number_barrier3d_models,
                        num_cores=num_cores,
                        beach_width_threshold=beach_width_threshold,
                        rmin=rmin,
                        rmax=rmax,
                        elevation_file=elevation_file,
                        dune_file=dune_file,
                        dune_design_elevation=dune_design_elevation,
                        dune_minimum_elevation=dune_minimum_elevation,
                        road_ele=road_ele,
                        road_width=road_width,
                        road_setback=road_setback,
                        group_roadway_abandonment=[0, 0, 0, 0, 0, 0, 1, 1, 1],
                        overwash_filter=overwash_filter,
                        overwash_to_dune=overwash_to_dune,
                        nourishment_volume=nourishment_volume,
                        background_erosion=background_erosion,
                        rebuild_dune_threshold=rebuild_dune_threshold,
                        roadway_management_on=roads_on,
                        beach_dune_manager_on=nourishments_on,
                        sea_level_rise_rate=sea_level_rise_rate,
                        sea_level_constant=sea_level_constant,
                    )

            one_hundred_thirds_acc_BE1m_ast_runs(
                storm_start=0,
                storm_end=100,
                name_prefix_1="9-CASCADE_AST_3domains_BE1m_AccSLR",
                name_prefix_2="9-CASCADE_AST_3domains_BE1m_AccSLR_nat_middle",
                storm_prefix="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_",
            )

            one_hundred_thirds_acc_BE1m_ast_runs(
                storm_start=0,
                storm_end=100,
                name_prefix_1="9-CASCADE_AST_3domains_BE1m_AccSLR_AdaptationScenario",  # whoops, meant to put future scenario
                name_prefix_2="9-CASCADE_AST_3domains_BE1m_AccSLR_nat_middle_AdaptationScenario",  # whoops, meant to put future scenario
                storm_prefix="StormSeries_1kyrs_VCR_Berm1pt9m_Slope0pt04_FutureScenario",
            )
