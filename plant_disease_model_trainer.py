import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os

print("TensorFlow Version:", tf.__version__)

# --- 1. Data Preparation ---
# Define the base directory where the dataset is located
base_dir = 'New Plant Diseases Dataset(Augmented)'
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'valid')

# Image dimensions
IMG_WIDTH = 224
IMG_HEIGHT = 224
BATCH_SIZE = 32

# Create ImageDataGenerators for data augmentation and normalization
# Augmentation helps prevent overfitting by creating modified versions of the images.
train_datagen = ImageDataGenerator(
    rescale=1.0/255.0,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# The validation data should not be augmented, only rescaled.
validation_datagen = ImageDataGenerator(rescale=1.0/255.0)

# Create data generators that flow images from the directories
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='categorical', # Use 'categorical' for multi-class classification
    shuffle=True
)

validation_generator = validation_datagen.flow_from_directory(
    validation_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

# Get the number of classes from the generator
num_classes = len(train_generator.class_indices)
print(f"Found {num_classes} classes.")
print("Class Indices:", train_generator.class_indices)


# --- 2. Model Definition (Using a more robust model like MobileNetV2 for transfer learning) ---
# Using a pre-trained model is more effective than building from scratch.
base_model = keras.applications.MobileNetV2(
    input_shape=(IMG_HEIGHT, IMG_WIDTH, 3),
    include_top=False, # Do not include the final classification layer
    weights='imagenet'
)

# Freeze the base model layers so we only train our new layers
base_model.trainable = False

# Add our custom classification layers on top of the pre-trained base
model = keras.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(512, activation='relu'),
    layers.Dropout(0.5), # Dropout helps prevent overfitting
    layers.Dense(num_classes, activation='softmax') # Softmax for multi-class probability
])

# --- 3. Model Compilation ---
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy', # Use for multi-class classification
    metrics=['accuracy']
)

model.summary()

# --- 4. Model Training ---
print("\nStarting model training...")
history = model.fit(
    train_generator,
    epochs=10, # For a real scenario, you might need more epochs
    validation_data=validation_generator
)
print("Model training finished.")

# --- 5. Save the Model ---
# Save the entire model to a single HDF5 file.
model.save('plant_disease_model.h5')
print("\nModel saved successfully as plant_disease_model.h5")

# --- 6. Model Evaluation ---
loss, accuracy = model.evaluate(validation_generator)
print(f'\nFinal Validation accuracy: {accuracy * 100:.2f}%')
