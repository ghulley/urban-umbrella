#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 16:36:39 2022

@author: madeleip
"""

#WRITE LAT, LON, VALUE NP ARRAY TO GEOTIFF

 
from osgeo import gdal, osr, ogr 
# import h5py
import numpy as np 
import scipy
from hytesinputs import *
import os

def getGeoTransform(extent, nlines, ncols):
    resx = (extent[2] - extent[0]) / ncols
    resy = (extent[3] - extent[1]) / nlines
    return [extent[0], resx, 0, extent[3] , 0, -resy]
 

def writegeotiff(data,lon,lat,fname):
    
    #Inputs 
    #Lon -np array of lon
    #Lat - 2d np array of lat
    # data - 2d np array of values 
    #fname - name of HyTES file 
    
    print('Beginning write file')
    
    #--------###Regrid to an even grid -----------------
    x1=np.min(lon)
    y1=np.min(lat)
    x2=np.max(lon)
    y2=np.max(lat)
    
    lnbnd=np.linspace(x1,x2,len(lon[:,0]))
    ltbnd=np.linspace(y1,y2,len(lat[0,:]))
    
    
    lon2,lat2=np.meshgrid(lnbnd,ltbnd)#create an evenly spaced grid
    lon2=np.transpose(lon2);lat2=np.transpose(lat2)
    
    #set border of 0
    newrow = np.zeros(len(data[:,0]))
    newcol = np.zeros(len(data[0,:]))
    
    A=data
    
    A[:,0]=newrow
    A[:,len(A[0,:])-1]=newrow
    
    A[0,:]=newcol
    A[len(A[:,0])-1,:]=newcol
    
    data=A
    
    #Regrid on a regular grid...
    data_interp = scipy.interpolate.griddata((lon.ravel(),lat.ravel()),data.ravel(),(lon2,lat2),'linear')


    #Now set 0 to nan 
    data_interp[data_interp==0]=np.nan
    
    #now apply these datasets for writing geotiff
    lon=lon2
    lat=lat2
    data = np.transpose(np.fliplr(data_interp))
    #------------##  --------------
    
    
    
    
    
    # Define the data extent (min. lon, min. lat, max. lon, max. lat)
    
    extent = [np.min(lon), np.min(lat), np.max(lon), np.max(lat)] #
    
    # Get GDAL driver GeoTiff
    driver = gdal.GetDriverByName('GTiff')
    
    # Get dimensions
    nlines = data.shape[0]
    ncols = data.shape[1]
    nbands = len(data.shape)
    data_type = gdal.GDT_Float32
    
    
    # Create a temp grid
    #options = ['COMPRESS=JPEG', 'JPEG_QUALITY=80', 'TILED=YES']
    grid_data = driver.Create('grid_data', ncols, nlines, 1, data_type)#, options)
     
    # Write data for each bands
    grid_data.GetRasterBand(1).WriteArray(data)
     
    # Lat/Lon WSG84 Spatial Reference System
    srs = osr.SpatialReference()
    srs.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
     
    # Setup projection and geo-transform
    grid_data.SetProjection(srs.ExportToWkt())
    grid_data.SetGeoTransform(getGeoTransform(extent, nlines, ncols))
     
    file_name = fname
    print(f'Generated GeoTIFF: {file_name}')
    driver.CreateCopy(file_name, grid_data, 0)  
    
    driver = None
    grid_data = None
     
    # Delete the temp grid
    import os                
    os.remove('grid_data')
    

if __name__ == '__main__':
    raw_hy_dir_path = r'F:\Documents\MATLAB\HyTES\Create geotiff\Example' # the directory that contains the hdf5 file, the geo.dat and the geo.hdr.
    hdf_f_path = os.path.join(raw_hy_dir_path,'20210525t212635_LosAngelesCA_L2_B103_V01.hdf5.hdf5')
    geo_dat_f_path = os.path.join(raw_hy_dir_path,'20210525t212635_LosAngelesCA_L1_B103_V01.geo.dat')
    geo_hdr_f_path = os.path.join(raw_hy_dir_path,'20210525t212635_LosAngelesCA_L1_B103_V01.geo.hdr')

    data,lat,lon = hytesinputs(hdf_f_path,geo_dat_f_path,geo_hdr_f_path)
    dst_dir = r'F:\Documents\MATLAB\HyTES\Create geotiff\Example'
    dst_path = os.path.join(dst_dir,'20210525t212635_LosAngelesCA_L2_B103_V01.tif')

    writegeotiff(data,lon,lat,dst_path)