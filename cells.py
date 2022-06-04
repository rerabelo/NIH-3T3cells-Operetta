import argparse
import cv2
import numpy as np
from matplotlib import pyplot as plt
from parso import parse
from scipy import ndimage
from skimage import measure, color, io, morphology, filters, segmentation
from skimage.segmentation import clear_border
from PIL import Image, ImageSequence
import multipagetiff as mtif
from tensorflow.keras.preprocessing import image
from scipy import ndimage as ndi

def getIncubationTime(filename):
    try:
        y = int(filename.split("/")[-1][:3])
        x = int(filename.split("/")[-1][3:6])
        if x == 2: 
            if y <= 4:
                return "15"
            elif y <= 7:
                return "60"
            else:
                raise Exception("Tempo de incubação desconhecido")
        elif x == 3:
            if y <= 4:
                return "120"
            elif y <= 7:
                return "15"
            else:
                raise Exception("Tempo de incubação desconhecido")
        elif x == 4:
            if y <= 4:
                return "60"
            elif y <= 7:
                return "120"
            else:
                raise Exception("Tempo de incubação desconhecido")
        elif x == 5:
            if y <= 4:
                return "15"
            elif y <= 7:
                return "60"
            else:
                raise Exception("Tempo de incubação desconhecido")
        elif x == 6:
            if y <= 4:
                return "120"
            elif y <= 7:
                return "15"
            else:
                raise Exception("Tempo de incubação desconhecido")
        elif x == 7:
            if y <= 4:
                return "60"
            elif y <= 7:
                return "120"
            else:
                raise Exception("Tempo de incubação desconhecido")
        elif x == 8:
            if y <= 4:
                return "15"
            elif y <= 7:
                return "60"
            else:
                raise Exception("Tempo de incubação desconhecido")
        elif x == 9:
            if y <= 4:
                return "120"
            elif y <= 7:
                return "15"
            else:
                raise Exception("Tempo de incubação desconhecido")
        elif x == 10:
            if y <= 4:
                return "60"
            elif y <= 7:
                return "120"
            else:
                raise Exception("Tempo de incubação desconhecido")
        elif x == 11:
            return "120"
        else:
            raise Exception("Tempo de incubação desconhecido")
    except Exception as e:
        print("Erro ao parsear nome do arquivo em getIncubationTime: {}".format(e))
        raise 


def getTratamentoparcial2 (filename):
    try:
        y = int(filename.split("/")[-1][:3])
        x = int(filename.split("/")[-1][3:6])
        
        if x == 2 or x == 7:
            return "N"
        elif x == 4 or x == 8 or x == 9:
            return "Z"          
        elif x == 5 or x == 10: 
            return "P"   
        elif x == 11: 
            return "CTRL" 
        elif x == 3:
            if y <= 4:
                return "N"
            elif y <= 7:
                return "Z"
            else:
                raise Exception("Tratamento desconhecido")
        elif x == 6:
            if y <= 4:
                return "P"
            elif y <= 7:
                return "N"
            else:
                raise Exception("Tempo de incubação desconhecido")
 
    except Exception as e:
        print("Erro ao parsear nome do arquivo em getTratamentoparcial2: {}".format(e))
        raise 


def getProteinaparcial2 (filename):
    try:
        y = int(filename.split("/")[-1][:3])
        x = int(filename.split("/")[-1][3:6])
        
        if x == 2 or x == 3 or x == 4 or x == 5:
            return "F"
        elif x == 7 or x == 8 or x == 9 or x == 10:
            return "B"          
        elif x == 6 or x == 11:
            if y <= 4:
                return "F"
            elif y <= 7:
                return "B"
            else:
                raise Exception("Proteina desconhecida")
        else:
            raise Exception("Proteina desconhecida") 
    except Exception as e:
        print("Erro ao parsear nome do arquivo em getProteinaparcial2: {}".format(e))
        raise 


def getIncubation(filename):
    if "T0H1" in filename:
        return "60"
    elif "T2H1" in filename:
        return "60"
    elif "T24H1" in filename:
        return "60"
    elif "T0H2" in filename:
        return getIncubationTime(filename)        
    else:
        "X"        
    
def getTime(filename):
    if "T0H1" in filename:
        return "0"
    elif "T0H2" in filename:
        return "0"    
    elif "T2H1" in filename:
        return "2"
    elif "T24H1" in filename:
        return "24"
    else:
        "X"

def getExperiment(filename):
    if "T0H1" in filename:
        return "1"
    elif "T2H1" in filename:
        return "1"
    elif "T24H1" in filename:
        return "1"
    elif "T0H2" in filename:
        return "2"        
    else:
        "X" 

def getTratamento(filename):
    if "T0H1" in filename:
        return getTratamentoparcial1(filename)
    elif "T0H2" in filename:
        return getTratamentoparcial2(filename)    
    elif "T2H1" in filename:
        return getTratamentoparcial1(filename)
    elif "T24H1" in filename:
        return getTratamentoparcial1(filename)
    else:
        "X"

def getProteina(filename):
    if "T0H1" in filename:
        return getProteinaparcial1(filename)
    elif "T0H2" in filename:
        return getProteinaparcial2(filename)    
    elif "T2H1" in filename:
        return getProteinaparcial1(filename)
    elif "T24H1" in filename:
        return getProteinaparcial1(filename)
    else:
        "X"

def getTratamentoparcial1(filename):
    try:
        x = int(filename.split("/")[-1][:3])
        y = int(filename.split("/")[-1][3:6])
               
        if x == 2 or x == 3:
            if y <= 4:
                return "N"
            elif y <= 7:
                return "Z"
            elif y <= 10:
                return "CTRL"
            else:
                raise Exception("Tratamento desconhecido")
        elif x == 4:
            if y <= 7:
                return "P"
            else:
                raise Exception("Tratamento desconhecido")
              
        else:
            raise Exception("Erro ao parsear primeira metade")
           
    except Exception as e:
        print("Erro ao parsear nome do arquivo em getTratamentoparcial1: {}".format(e))
        raise

def getProteinaparcial1(filename):
    try:
        x = int(filename.split("/")[-1][:3])
        y = int(filename.split("/")[-1][3:6])
        
        if x == 2:
            return "F"
        elif x == 3:
            return "B"
        elif x == 4:
            if y <= 4:
                return "F"
            elif y <= 7:
                return "B"
            else:
                raise Exception("Proteina desconhecida")       
        else:
            raise Exception("Erro ao parsear primeira metade")
        
    except Exception as e:
        print("Erro ao parsear nome do arquivo em getProteinaparcial1: {}".format(e))
        raise


def parseFile(file, prefix):
  # Read image 
  original_img = mtif.read_stack(file)

  green_channel=original_img[1]

  # Thresholding: Determining the borders of the cells. This first thresholding function estimates the locations of the cells.
  pixels_to_um = 0.49661 # 1 pixel = 496 nm (got this from the metadata of original image)

  # Threshold image
  thresh = filters.threshold_mean(green_channel)  # See "Available threshold filters"
  threshold_img = green_channel.copy()
  threshold_img[(green_channel > thresh)==False] = 0
  threshold_img[(green_channel > thresh)==True] = 65535

  # Available threshold filters
  # https://scikit-image.org/docs/stable/api/skimage.filters.html?highlight=skimage%20filters#module-skimage.filters
  # https://imagej.net/plugins/auto-threshold

  # Closing operations: keep the size of the cells in the mask roughly the same while refining their shape. The gaps in cell structure are filled in.
  closing = morphology.closing(threshold_img)
  # Morphology closing and opening
  # https://canvas.colorado.edu/courses/61439/pages/morphological-opening-and-closing#:~:text=Morphological%20closing%20is%20a%20dilation,close%20gaps%20in%20the%20image.

  # Deleting cells in the border of the image.
  clear_border_img = clear_border(closing) # Remove edge 
  # Clear_border
  # https://scikit-image.org/docs/dev/api/skimage.segmentation.html

  # Removing artifacts and non-viable cells using a filter of size. Herein, only structures with a size bigger than 2000 pixels^2 are kept to continue the analysis.
  # Settings
  small_objects_removed = morphology.remove_small_objects(measure.label(clear_border_img), min_size=2000) # 512 Artifacts / 2000 cells
  # Settings
  clear_border_img[small_objects_removed == 0] = 0

  # Extracting the area of sure foreground:

  # 1) Calculating the distance from foregrounds points to the nearest background point. A binary image is transformed into a grayscale image analogous to a relief.

  # 2) Determining the cells limite

  dist_transform = ndi.distance_transform_edt(clear_border_img)
  # dist_transform
  # https://docs.opencv.org/3.4/d2/dbd/tutorial_distance_transform.html
  # https://www.tutorialspoint.com/opencv/opencv_distance_transformation.htm

  ret2, sure_fg = cv2.threshold(dist_transform,0.01*dist_transform.max(),65535,0)
  sure_fg = np.uint16(sure_fg)

  # Extracting the area of sure background: The clear_border image is dillated, removing the boundary region.
  kernel = np.ones((3,3),np.uint16)
  sure_bg = cv2.dilate(clear_border_img,kernel,iterations=10)
  sure_bg = np.uint16(sure_bg) 

  # Subtracting the sure background and the sure foreground: the remaining region is unknown (is it cell or background?)
  unknown = cv2.subtract(sure_bg,sure_fg) 
  # Labeling the regions: each isolated cell region is labelled with a different number (0 = background)

  # Now we create a marker and label the regions inside. 
  # For sure regions, both foreground and background will be labeled with positive numbers.
  # Unknown regions will be labeled 0. 
  # For markers let us use ConnectedComponents. 
  markers = measure.label(sure_fg)
  # Marking the background as 1 and the unknown region as 0.
  markers = markers + 10
  # Now, mark the region of unknown with zero
  markers[unknown==65538] = 0

  # Now we are ready for watershed filling
  markers = segmentation.watershed(green_channel, markers)
  img2 = color.label2rgb(markers, bg_label=0)

  # The boundary region will be marked -1
  # https://docs.opencv.org/3.3.1/d7/d1b/group__imgproc__misc.html#ga3267243e4d3f95165d55a618c65ac6e1

  # Measuring the fluorescence intensity (Cells - Mask 1)

  # Red channel:
  # Extract red channel
  red_channel=original_img[2] # Image equivalent to grey image.
  img = red_channel.copy()
  # Measuring mean fluorescence intensity.
  regions = measure.regionprops(markers, intensity_image=red_channel)
  # regions = measure.regionprops(markers, intensity_image=green_channel)
  # https://scikit-image.org/docs/stable/auto_examples/segmentation/plot_regionprops.html

  #for prop in regions:
  #    print('Label: {} Area: {} MinIntensity: {} MeanIntensity: {} MaxIntensity: {}'.format(prop.label, prop.area, prop.min_intensity, prop.mean_intensity, prop.max_intensity))
      
  propList = ['Area',
              'MinIntensity',
              'MeanIntensity',
              'MaxIntensity'] 

  # Saving the file
  output_file = open(prefix + '_cell_measurements.csv', 'a')
  # output_file.write("," + ",".join(propList) + '\n') # join strings in array by commas, leave first cell blank
  # First cell blank to leave room for header (column names)

  cell_number = 0
  for region_props in regions:
      #output cluster properties to the excel file
      output_file.write(file)
      output_file.write(',' + str(cell_number))
      for i,prop in enumerate(propList):
          if(prop == 'Area'): 
              to_print = region_props[prop]*pixels_to_um**2   #Convert pixel square to um square
          elif(prop == 'orientation'): 
              to_print = region_props[prop]*57.2958  #Convert to degrees from radians
          elif(prop.find('Intensity') < 0):          # Any prop without Intensity in its name
              to_print = region_props[prop]*pixels_to_um
          else: 
              to_print = region_props[prop]     # Reamining props, basically the ones with Intensity in its name
          output_file.write(',' + str(to_print))
      output_file.write(', ' + getExperiment(file))           
      output_file.write(', ' + getIncubation(file))           
      output_file.write(', ' + getTratamento(file))   
      output_file.write(', ' + getProteina(file))
      output_file.write(', ' + getTime(file))      
      output_file.write('\n')
      cell_number += 1
      
  output_file.close()

  # Measuring the fluorescence intensity (Mask 2)
  not_closing = closing.copy()
  not_closing[closing == 0] = 65535
  not_closing[closing == 65535] = 0

  not_dist_transform = ndi.distance_transform_edt(not_closing)
  # dist_transform
  # https://docs.opencv.org/3.4/d2/dbd/tutorial_distance_transform.html
  # https://www.tutorialspoint.com/opencv/opencv_distance_transformation.htm

  ret3, not_sure_fg = cv2.threshold(not_dist_transform,0.01*not_dist_transform.max(),65535,0)
  not_sure_fg = np.uint16(not_sure_fg)

  kernel = np.ones((3,3),np.uint16)
  not_sure_bg = cv2.dilate(not_closing,kernel,iterations=10)
  not_sure_bg = np.uint16(not_sure_bg) 

  unknown2 = cv2.subtract(not_sure_bg,not_sure_fg)
  ret3, not_sure_fg = cv2.threshold(not_dist_transform,0.01*dist_transform.max(),65535,0)
  not_sure_fg = np.uint16(not_sure_fg)

  # Extract red channel
  red_channel=original_img[2] # Image equivalent to grey image.
  img = red_channel.copy()

  regions = measure.regionprops(not_sure_fg, intensity_image=red_channel)
  # regions = measure.regionprops(markers, intensity_image=green_channel)
  # https://scikit-image.org/docs/stable/auto_examples/segmentation/plot_regionprops.html

  # for prop in regions:
  #     print('Label: {} Area: {} MinIntensity: {} MeanIntensity: {} MaxIntensity: {}'.format(prop.label, prop.area, prop.min_intensity, prop.mean_intensity, prop.max_intensity))
      
  propList = ['Area',
              'MinIntensity',
              'MeanIntensity',
              'MaxIntensity'] 

  output_file = open(prefix + '_background.csv', 'a')
  # output_file.write(',' + ",".join(propList) + '\n') # join strings in array by commas, leave first cell blank
  # First cell blank to leave room for header (column names)

  background = 1
  for region_props in regions:
      #output cluster properties to the excel file
      output_file.write(file)
      output_file.write(',' + str(background))
      for i,prop in enumerate(propList):
          if(prop == 'Area'): 
              to_print = region_props[prop]*pixels_to_um**2   #Convert pixel square to um square
          elif(prop == 'orientation'): 
              to_print = region_props[prop]*57.2958  #Convert to degrees from radians
          elif(prop.find('Intensity') < 0):          # Any prop without Intensity in its name
              to_print = region_props[prop]*pixels_to_um
          else: 
              to_print = region_props[prop]     # Reamining props, basically the ones with Intensity in its name
          output_file.write(',' + str(to_print))
      output_file.write(', ' + getExperiment(file))           
      output_file.write(', ' + getIncubation(file))           
      output_file.write(', ' + getTratamento(file))   
      output_file.write(', ' + getProteina(file))
      output_file.write(', ' + getTime(file)) 
      output_file.write('\n')
      background += 1
      
  output_file.close()


  # Find number of nuclei

  blue_channel = original_img[0]

  # GET BLUE IMAGE - will be user to find number of nuclei
  nuclei = blue_channel.copy()
  nuclei[sure_fg == 0] = 0

  pixels_to_um = 0.49661 # 1 pixel = 496 nm (got this from the metadata of original image)
  nuclei_thresh = filters.threshold_otsu(nuclei)
  threshold_nuclei = nuclei.copy()
  threshold_nuclei[(nuclei > nuclei_thresh)==False] = 0
  threshold_nuclei[(nuclei > nuclei_thresh)==True] = 65535

  nuclei_dist_transform = ndi.distance_transform_edt(threshold_nuclei)

  ret2, nuclei_sure_fg = cv2.threshold(nuclei_dist_transform,0.35*nuclei_dist_transform.max(),65535,0)
  nuclei_sure_fg = np.uint16(nuclei_sure_fg)

  kernel = np.ones((3,3),np.uint16)
  nuclei_sure_bg = cv2.dilate(threshold_nuclei,kernel,iterations=10)
  nuclei_sure_bg = np.uint16(nuclei_sure_bg)

  nuclei_unknown = cv2.subtract(nuclei_sure_bg,nuclei_sure_fg)

  nuclei_label = measure.label(nuclei_sure_fg)
  nuclei_label = nuclei_label+1
  nuclei_label[nuclei_unknown==65538] = 0

  nuclei_lable = segmentation.watershed(blue_channel, nuclei_label)
  nuclei_img2 = color.label2rgb(nuclei_label, bg_label=0)
  plt.imshow(nuclei_img2)
  nuclei_img2.dtype

  regions = measure.regionprops(nuclei_lable, intensity_image=nuclei)

  propList = ['Area',
              'equivalent_diameter', #Added... verify if it works
              'orientation', #Added, verify if it works. Angle btwn x-axis and major axis.
              'eccentricity', # When it is 0, the ellipse becomes a circle.
              'MajorAxisLength',
              'MinorAxisLength',
              'Perimeter',
              'MinIntensity',
              'MeanIntensity',
              'MaxIntensity']
              

  with open(prefix + '_xxx.csv', 'a') as output_file:
    nuclei_number = 0
    for region_props in regions:
        #output cluster properties to the excel file
        output_file.write(file)
        output_file.write(',' + str(nuclei_number))
        for i,prop in enumerate(propList):
            if(prop == 'Area'): 
                to_print = region_props[prop]*pixels_to_um**2   #Convert pixel square to um square
            elif(prop == 'orientation'): 
                to_print = region_props[prop]*57.2958  #Convert to degrees from radians
            elif(prop.find('Intensity') < 0):          # Any prop without Intensity in its name
                to_print = region_props[prop]*pixels_to_um
            else: 
                to_print = region_props[prop]     # Reamining props, basically the ones with Intensity in its name
            output_file.write(',' + str(to_print))
        output_file.write(', ' + getExperiment(file))           
        output_file.write(', ' + getIncubation(file))           
        output_file.write(', ' + getTratamento(file))   
        output_file.write(', ' + getProteina(file))
        output_file.write(', ' + getTime(file))        
        output_file.write('\n')
        nuclei_number += 1
        
    # print(nuclei_number-1) # (-1) resctive to mean (Line 1 -> dataset)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("file")
  parser.add_argument("prefix")
  args = parser.parse_args()

  parseFile(args.file, args.prefix)