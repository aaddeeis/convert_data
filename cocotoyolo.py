import os
import shutil
from os import walk, getcwd
from PIL import Image
def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)
    
    
"""-------------------------------------------------------------------""" 
""" Configure Paths"""   
mypath = "F:/Project Prof Siti/aaddeeis/DR RIA NOVA/YOLO/CONVERT DATA/CONVERT COCO TO YOLO TXT/DATA/HOLE/val/"
outpath = "F:/Project Prof Siti/aaddeeis/DR RIA NOVA/YOLO/CONVERT DATA/CONVERT COCO TO YOLO TXT/SIMPAN/HOLE/val/"
json_backup ="F:/Project Prof Siti/aaddeeis/DR RIA NOVA/YOLO/CONVERT DATA/CONVERT COCO TO YOLO TXT/BACKUP/HOLE/val/"

wd = getcwd()
#list_file = open('%s_list.txt'%(wd), 'w')
'''correct .JPG to .jpg'''
#os.rename(old_name, new_name)
""" Get input json file list """
json_name_list = []
for file in os.listdir(mypath):
    if file.endswith(".json"):
        json_name_list.append(file)
    if '.JPG' in file:
        os.rename(mypath+'/'+file, mypath+'/'+file.strip('.JPG')+'.jpg')
    
""" Process """
for json_name in json_name_list:
    txt_name = json_name.rstrip(".json") + ".txt"
    """ Open input text files """
    txt_path = mypath +'/' + json_name
    print("Input:" + txt_path)
    txt_file = open(txt_path, "r")
    
    """ Open output text files """
    txt_outpath = outpath + '/'+ txt_name
    print("Output:" + txt_outpath)
    txt_outfile = open(txt_outpath, "a+")
    """ Create a label dictionary."""
    label_dic={'H': 0} #hole
    # label_dic={'LA': 0, 'LV': 1, 'RA': 2, 'RV': 3} #4CH
    # label_dic={'RA': 0, 'LA': 1, 'LV': 2, 'RV': 3} #SUB
    # label_dic={'H': 0, 'A': 1, 'RA': 2, 'RVOT': 3, 'PA': 4, 'LA' :5} #SA
    # label_dic={'H': 0, 'LA': 1, 'A': 2, 'RV': 3, 'LV': 4} #LA
    # label_dic={'H': 0, 'A': 1, 'RV': 2, 'LA': 3, 'RA': 4, 'LV': 5} # 5CH
    """ Convert the data to YOLO format """ 
    lines = txt_file.read().split() #'\r\n'  #for ubuntu, use "\r\n" instead of "\n"
    for idx, line in enumerate(lines):
        if ("lineColor" in line):
            break     #skip reading after find lineColor
        if ("label" in line):
            idxlist=[element for element in range(5,90,4)] #[5,9,13,17,21,25,29,33,37,41,45...]
            pl=list() #list of polygon points
            try:
                for i in idxlist:
                    pl.append((float(lines[idx+i].rstrip(',')), float(lines[idx+i+1])))
                    cob=label_dic[lines[idx+1].rstrip(',').strip('"')]
            except:
                pass
            #print('pl: ',pl)
            #in case when labelling, points are not in the right order
            xmin=9999999
            xmax=0
            ymin=9999999
            ymax=0
            for (x,y) in pl:
              if x<xmin:
                xmin=x
              if x>xmax:
                xmax=x
              if y<ymin:
                ymin=y
              if y>ymax:
                ymax=y
            img_path = str('%s/%s.jpg'%(mypath, os.path.splitext(json_name)[0]))
            im=Image.open(img_path)
      
            w= int(im.size[0])
            h= int(im.size[1])
        
            
            print(w, h)
            print(xmin, xmax, ymin, ymax)
            b = (xmin, xmax, ymin, ymax)
            bb = convert((w,h), b)
            print('CLASS', cob)
            print(bb)
            txt_outfile.write(str(cob) + " " + " ".join([str(a) for a in bb]) + '\n')
           
       
    shutil.copy(txt_path,json_backup+'/'+json_name)    #move json file to backup folder