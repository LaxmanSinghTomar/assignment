# Model Utilities and Inference Function

# Importing Libraries
from tensorflow import keras
from PIL import Image
from io import BytesIO
import numpy as np
import pathlib
import os


class Utils():
    def __init__(self, logger, model_path):
        self.logger = logger
        self.model_path = model_path
        self.model = self.load_model()
        self.classes = {0: 'T-Shirt/top',
                            1: 'Trouser',
                            2: 'Pullover',
                            3: 'Dress',
                            4: 'Coat',
                            5: 'Sandal',
                            6: 'Shirt',
                            7: 'Sneaker',
                            8: 'Bag',
                            9: 'Ankle boot'}


    def load_model(self):
        """
        Load Model using the provided "model_path".

        Returns:
            Loaded Model.
        """
        path = pathlib.Path(__file__).resolve().parent.parent.parent
        print(path)
        model = keras.models.load_model(os.path.join(path, self.model_path))
        return model
    

    def img_to_array(self, imageStream):
        """
        Convert Incoming Image to Numpy Array.

        Args:
            imageStream: Incoming Image from Stream.
        
        Returns:
            An array representation of Image.
        """
        try:
            stream = BytesIO(imageStream)
            image = Image.open(stream)
            image = np.asarray(image)
            return image
        except Exception as e:
            self.logger.warning(f"Sorry! Failed to convert the image to numpy array.{e}")
            return None


    def get_message_images(self, messageList):
        """
        Get Images from Incoming Message List and Push RequestID, Images to the queue.

        Args:
            messageList: Incoming MessageList

        Returns:
            None
        """
        successImages, successReqID = np.array([]), np.array([])
        for item in messageList:
            try:
                requestID = item['requestID']
                image = self.img_to_array(imageStream=item['image'])
                if image is not None:
                    successImages = np.append(successImages, image)
                    successReqID = np.append(successReqID, [requestID])
                    return successReqID, successImages
            except Exception as e:
                self.logger.error(f"Failed to consume messages!{e}")
                return None, None
    

    def inference(self, consumedMessage=[]):
        """
        Make an Inference using Message from Consumer.

        Args:
            consumedMessage: Incoming Message from Consumer.

        Returns:
            Request ID, and predicted Class Label.
        """
        if len(consumedMessage) <= 0:
            return None
        requestID, imageStream = self.get_message_images(messageList= consumedMessage)

        self.logger.info("Reshaping/Normalizing Images for the CNN Model...")
        imageStream = imageStream.reshape((imageStream.shape[0], 28, 28, 1))
        imageStream /= 255.0

        self.logger.info("Predicting Class Labels for Images...")
        preds = self.model.predict_classes(imageStream)

        classLabelName = []
        for classLabel in preds:
            classLabelName.append(self.classconfig[classLabel])

        return requestID, classLabelName