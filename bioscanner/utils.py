import io
import base64
import base64
from io import BytesIO
from PIL import Image
from PIL import Image, ImageDraw
import requests
import json
import numpy as np 
#import base64
#from PIL import Image
#from io import BytesIO

#ip = "192.168.0.126:5000"
ip = "localhost:5001"

#we need to encapsulate the code into functions to be reusable. 
def b64_to_PIL(data):
    """
    This function takes a b64 code and convert it 
    into PIL Image object, it reads the size of the imge 

    - Input: b64 information 
    - Output : w, h, img object  
    """
    im_bytes = base64.b64decode(data)   # im_bytes is a binary image
    im_file = BytesIO(im_bytes)  # convert image to file-like object
    img = Image.open(im_file) 
    w, h = img.size

    return w,h,img 


def draw_rectangle(object,w,h,pred):
    """
    This function draws a rectangle over an image
    - input: 
    """
    startX = int(pred[0] * w)
    startY = int(pred[1] * h)
    endX = int(pred[2] * w)
    endY = int(pred[3] * h)
    shape = [(startX, startY), (endX,endY)]
  
    # creating new Image object
    #img = Image.new("RGB", (w, h))
  
    # draw  rectangle in the image
    img1 = ImageDraw.Draw(object)  
    img1.rectangle(shape, outline ="red",width=10)
    #img.show()
    return object


def PIL_to_b64(data):
    """
    This functions receices a PIL object which has been 
    edited with a rectangle and parse it to b64, so we 
    can send it to the computer 
    - input: 

    
    """
    buffer = BytesIO()
    data.save(buffer,format="JPEG")
    myimage = buffer.getvalue()
    img = base64.b64encode(myimage)
    return img



def img_to_base64_str(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)
    img_byte = buffered.getvalue()
    img_str = base64.b64encode(img_byte).decode()
    return img_str

def save_base64_to_png(base64_string, output_path):
    # Remove the data URL prefix if it exists (e.g., "data:image/png;base64,")
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]
    
    # Decode the base64 string
    image_data = base64.b64decode(base64_string)
    
    # Write the binary data to a file
    with open(output_path, 'wb') as f:
        f.write(image_data)
    return True

#########################################################
#       Obj det  function to request the API            #
########################################################
def query_api(data):
    my_ip = ip 
    end_point ="http://"+my_ip+"/models/objectD"
    #requests post method
    resp = requests.post(end_point, json=data)
    
    return resp.json()["Resultados"]


########################################################
#     Individuals Functions to query the API           #
########################################################

def query_indv_api(data):
    my_ip = ip 
    end_point ="http://"+my_ip+"/models/indvembed"
    #data = conv
    #requests post method
    resp = requests.post(end_point, json=data)
    #print(resp.text)
    return resp
    

def response_indv_view(resp):
    #this function aims to read the resonse of the API of inference
    #this goes in DJANGO to receive the API output 
    # Parse the JSON data
    data = json.loads(resp.text)
    # Extract the base64-encoded image
    encoded_image = data.get("img")
    # Remove the 'b' prefix if it exists
    #in the django view we need to send 
    #encoded_image to the html to be rendered 
    encoded_image = encoded_image.strip("b'")
    # Decode the base64-encoded image
    #image_data = base64.b64decode(encoded_image)
    # Create a PIL Image from the decoded image data
    #image = Image.open(BytesIO(image_data))
    # Display the image
    #image.show()
    #plt.imshow(image)
    #plt.axis('off')  # Optional: Turn off axis labels and ticks
    #plt.show()
    embed = np.array([float(x) for x in data["embed"].replace("[","").replace("]","").split(",")])
    return encoded_image,embed 
    
    
    
############################################################
#           classification                                 #
############################################################


def query_class_api(data):
    my_ip = ip 
    end_point ="http://"+my_ip+"/models/prediction"
    #data = conv
    #requests post method
    resp = requests.post(end_point, json=data)
    #print(resp.text)
    return resp


def get_label_class(conv):

    rep334 = query_class_api(conv)
    data22 = json.loads(rep334.text)

    lab = ["Jaguar","No-Jaguar"]

    ind = np.argmax(data22["Resultados"])

    return lab[ind]