#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 23:12:59 2022

@author: sau
"""

from bse_seg import *

if __name__ == '__main__':
    
    # Get a list of available datasets
    dataset_names = ['dataset1', 'dataset2', 'dataset3', 'dataset4']
    folder = os.getcwd()
    datasets = [f for f in dataset_names if os.path.isdir(os.path.join(folder, f))]
    if not datasets:
        print('No datasets are available! Exiting..')
        sys.exit(1)
        
    
    # Loop through the datasets
    for dataset in datasets:
        # Check if the subfolder with BSE images exists for the current dataset
        bse_folder = os.path.join(folder, dataset, 'BSE')
        if not os.path.isdir(bse_folder):
            print(bse_folder + ' not found..')
            continue
        
        
        # Create the folder for segmented BSE images
        bse_seg_folder = os.path.join(folder, dataset, 'BSE_segmented')
        try:
            if os.path.isdir(bse_seg_folder):
                print('\nDeleting everything in ' + str(bse_seg_folder) + '\n')
                shutil.rmtree(bse_seg_folder)
            os.mkdir(bse_seg_folder)
        except Exception as e:
            print('Failed to create %s. Reason: %s' % (bse_seg_folder, e))
            continue
        
        
        # Write the header to the results file
        resfile = os.path.join(folder, dataset, 'results_' + dataset + '.csv')
        try:
            with open(resfile, 'w') as csvfile:
                csvfile.write('path,quartz_rel_area,pores_rel_area,otherminerals_rel_area\n')
        except Exception as e:
            print('Failed to create %s. Reason: %s' % (resfile, e))
            continue
        
        
        # Loop through all BSE files and segment them
        for root, dirs, files in os.walk(bse_folder):
            
            for file in files:
                # Read the current BSE image using OpenCV
                try:
                    bse = cv2.imread(os.path.join(bse_folder, file))
                except Exception as e:
                    print('Failed to open %s. Reason: %s' % (os.path.join(bse_folder, file), e))
                    continue
                
                # Segment the CL image
                bse_seg, rel_areas = segment(bse)

                # Saving the segmented BSE image
                try:
                    cv2.imwrite(os.path.join(bse_seg_folder, file), bse_seg)
                except Exception as e:
                    print('Failed to save %s. Reason: %s' % (os.path.join(bse_seg_folder, file), e))
                    continue

                # Keep the earlier saved results
                lines = []
                if os.path.isfile(resfile):
                    with open(resfile, 'rt') as csvfile:
                        lines = csvfile.readlines()

                # Update the results with the current segmented BSE image
                result = os.path.join(bse_folder, file) + ',' + ','.join(str(rel_area) for rel_area in rel_areas) + '\n'
                with open(resfile, 'wt') as csvfile:
                    lines.append(result)
                    for l in lines:
                        csvfile.write(l)
    