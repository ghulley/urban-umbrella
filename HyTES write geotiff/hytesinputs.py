#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 15:02:23 2022

@author: madeleip
"""
import h5py
import numpy as np
import sys


def hytesinputs(fL2, fgeo, fgeohdr):
    
    #Input HDR/HDF/.dat 
    #inputs:
        #LOC     : path of file
        #fL2     : name of hdf file
        #fgeo    : name of geo.dat file 
        #fgeohdr : name of header file 
        
    #OUTPUT 
    #NP ARRAYS
        #TS     : LST (K)
        #etas   : EMISS
        #lathyf : Lat Hyf (dec deg)
        #lonhyf : Lon Hyf (dec deg)
    
    
    
    #FOR THE PURPOSE OF THE EXAMPLE .... 
    # HyTES location
    loc='F:/Documents/MATLAB/HyTES/Create geotiff/Example/'

    # # Eg file names 
    fL2 = loc + '20210525t212635_LosAngelesCA_L2_B103_V01.hdf5';
    fgeo = loc+'20210525t212635_LosAngelesCA_L1_B103_V01.geo.dat';
    fgeohdr = loc+'20210525t212635_LosAngelesCA_L1_B103_V01.geo.hdr';





    #Hytes Header Info 
    fid = open(fgeohdr)
    lin=fid.readline().rstrip()
    lin=fid.readline().rstrip()
    lin=fid.readline().rstrip()
    lin=fid.readline().rstrip()
    
    tok,rem=lin.split('=')
    cols = int(rem) #get number of cols 
    
    lin=fid.readline().rstrip()
    tok,rem=lin.split('=')
    rows = int(rem) #get number of rows 
   
    lin=fid.readline().rstrip()
    lines,rem=lin.split('=')
    bands = int(rem)
    
    
    
    
    #Hytes Geo File geo.dat
    geo = open(fgeo, 'r')
    geo=np.fromfile(geo,np.float32)
    bgeo = 4
    
    geo = np.reshape(geo,(bgeo,cols,rows),order='F')
    
    geo=np.transpose(geo)
    geo = np.double(geo)
    
    
    # Sensor altitude in meters
    #Hgt = double(hdf5read(L1info.GroupHierarchy.Groups(1).Datasets(4)));
    #Hgt = mean(Hgt(:))./1000; % Average and convert to km
    
    # DEM
    DEM = geo[:,:,2]
    DEM = np.mean(DEM)/1000
     
    #Lat and Lon 
    LatHyf = geo[:,:,0]
    LonHyf = geo[:,:,1]

    #size 
    szh=np.shape(LatHyf)
    

    
    #Read in HyTES
    

    f = h5py.File(fL2, 'r')
    
    #get key of fL2
    hyteskey=list(f.keys())
    #import LST with either key 
    if 'L2_LST' in hyteskey:
        LST = f['L2_LST']
    if 'l2_land_surface_temperature' in hyteskey:
        LST=f['l2_land_surface_temperature']
    
   # if 'l2_land_surface_temperature' not in hyteskey and 'L2_LST' not in hyteskey:
    #    print('Temp not found in hdf5 file. exiting...')
        
        
    LST = np.asarray(LST)#convert to np array
    
    
    #remove data that is less 0
    LST=np.where(LST<0, np.nan,LST)
    
    #LST=np.fillmissing(LST,'nearest');
    # if 'L2_Emissivity' in hyteskey:
    #     emis = f['L2_Emissivity']
    # if 'l2_emissivity' in hyteskey:
    #     emis=f['l2_emissivity']
    # emis =np.asarray(emis)
    

    # if 'L2_Emissivity_Wavelengths' in hyteskey:
    #     emiswave = f['L2_Emissivity_Wavelengths'];  # Read Emissivity wavelengths
    # if 'l2_emissivity_wavelengths' in hyteskey:
    #     emiswave = f['l2_emissivity_wavelengths']; 
    
    
    # emiswave = np.asarray(emiswave)
    # w = emiswave*10**-6

    szL2 = np.shape(LST)
    
 


    # Broadband emissivity calculation
    # Tf = 300;
    # c1 = 3.7418e-22;
    # c2 = 0.014388;
    # BBE = np.zeros(szL2);Bn1=np.sum(emis*(c1/(w**5*np.pi*(np.exp(c2/(w*Tf))-1))),2);Bn2 = sum(c1/(w**5*np.pi*(np.exp(c2/(w*Tf))-1)));BBE=Bn1/Bn2;BBEff=BBE;

  #  for i in range(0,szh[0]):
    
   #     for j in range(0,szh[1]):
        
    #        e = np.squeeze(emis[i,j,:]);
    
     #       Bnum = e*(c1/(w**5*np.pi*(np.exp(c2/(w*Tf))-1)));
      #      Bdem = c1/(w**5*np.pi*(np.exp(c2/(w*Tf))-1));
                   
       #     BBE[i,j] = sum(Bnum)/sum(Bdem);
   # BBEff = BBE;

    
    maxLat = np.max(LatHyf[:])
    minLat = np.min(LatHyf[:])
    maxLon = np.max(LonHyf[:])
    minLon = np.min(LonHyf[:])



    #Sometimes Lat/Lon and L1/L2 don't have same number of lines so resize for now
    LatHyf = np.resize(LatHyf,szL2)
    LonHyf = np.resize(LonHyf,szL2)
    

    #RETURN HYTES VARS

    TS = LST        #LST K
    # etas = BBEff    #Surface Emissivity 
    
    
    #a test
 
    return TS,LatHyf, LonHyf  

    




