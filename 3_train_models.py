"""
CNN Model Training - ResNet50 and EfficientNetB0
Category B - Project 2: Pakistani Politician Image Classification
Minimum 2 models required
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.applications import ResNet50, EfficientNetB0
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from pathlib import Path
import json
import pickle
from datetime import datetime

class ModelTrainer:
    """Train and save CNN models"""
    
    def __init__(self, img_size=224, batch_size=32, epochs=30):
        self.img_size = img_size
        self.batch_size = batch_size
        self.epochs = epochs
        self.class_names = None
        self.num_classes = None
        self.history = {}
        
    def get_data_generators(self, train_dir, val_dir, test_dir):
        """Create data generators with preprocessing"""
        
        # ImageNet preprocessing for pretrained models
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            preprocessing_function=self._get_preprocessing_fn()
        )
        
        val_datagen = ImageDataGenerator(
            rescale=1./255,
            preprocessing_function=self._get_preprocessing_fn()
        )
        
        test_datagen = ImageDataGenerator(
            rescale=1./255,
            preprocessing_function=self._get_preprocessing_fn()
        )
        
        # Load data
        train_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=(self.img_size, self.img_size),
            batch_size=self.batch_size,
            class_mode='categorical',
            shuffle=True
        )
        
        val_generator = val_datagen.flow_from_directory(
            val_dir,
            target_size=(self.img_size, self.img_size),
            batch_size=self.batch_size,
            class_mode='categorical',
            shuffle=False
        )
        
        test_generator = test_datagen.flow_from_directory(
            test_dir,
            target_size=(self.img_size, self.img_size),
            batch_size=self.batch_size,
            class_mode='categorical',
            shuffle=False
        )
        
        self.class_names = list(train_generator.class_indices.keys())
        self.num_classes = len(self.class_names)
        
        return train_generator, val_generator, test_generator
    
    def _get_preprocessing_fn(self):
        """Return preprocessing function for model"""
        return None  # Will be set per model
    
    def build_resnet50(self):
        """Build ResNet50 model"""
        
        base_model = ResNet50(
            input_shape=(self.img_size, self.img_size, 3),
            include_top=False,
            weights='imagenet'
        )
        
        # Freeze base model
        base_model.trainable = False
        
        model = models.Sequential([
            layers.Input(shape=(self.img_size, self.img_size, 3)),
            layers.Lambda(lambda x: tf.keras.applications.resnet50.preprocess_input(x)),
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dense(512, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        return model
    
    def build_efficientnet_b0(self):
        """Build EfficientNetB0 model"""
        
        base_model = EfficientNetB0(
            input_shape=(self.img_size, self.img_size, 3),
            include_top=False,
            weights='imagenet'
        )
        
        # Freeze base model
        base_model.trainable = False
        
        model = models.Sequential([
            layers.Input(shape=(self.img_size, self.img_size, 3)),
            layers.Lambda(lambda x: tf.keras.applications.efficientnet.preprocess_input(x)),
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dense(512, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        return model
    
    def train_model(self, model, model_name, train_generator, val_generator, output_dir="models"):
        """Train model and save"""
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        print(f"\n{'='*70}")
        print(f"Training: {model_name}")
        print(f"{'='*70}")
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=1e-4),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Callbacks
        early_stop = keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True
        )
        
        reduce_lr = keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            min_lr=1e-7,
            verbose=1
        )
        
        model_checkpoint = keras.callbacks.ModelCheckpoint(
            output_path / f"{model_name}_best.h5",
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        )
        
        # Train
        history = model.fit(
            train_generator,
            validation_data=val_generator,
            epochs=self.epochs,
            callbacks=[early_stop, reduce_lr, model_checkpoint],
            verbose=1
        )
        
        # Save model
        model.save(output_path / f"{model_name}_final.h5")
        
        # Save history
        with open(output_path / f"{model_name}_history.pkl", 'wb') as f:
            pickle.dump(history.history, f)
        
        print(f"\n✓ {model_name} training complete!")
        print(f"  Model saved: {output_path / f'{model_name}_final.h5'}")
        
        self.history[model_name] = history.history
        
        return model, history

def main():
    """Main training pipeline"""
    
    print("\n" + "="*70)
    print("🧠 CNN MODEL TRAINING")
    print("Pakistani Politician Image Classification")
    print("="*70)
    
    # Paths
    TRAIN_DIR = "dataset_split/train"
    VAL_DIR = "dataset_split/val"
    TEST_DIR = "dataset_split/test"
    OUTPUT_DIR = "models"
    
    # Check if dataset exists
    if not all(Path(d).exists() for d in [TRAIN_DIR, VAL_DIR, TEST_DIR]):
        print("❌ Dataset split not found!")
        print("   Run '1_split_dataset.py' first")
        return
    
    # Configuration
    IMG_SIZE = 224
    BATCH_SIZE = 32
    EPOCHS = 30
    
    # Initialize trainer
    trainer = ModelTrainer(img_size=IMG_SIZE, batch_size=BATCH_SIZE, epochs=EPOCHS)
    
    # Get data generators
    print("\n📁 Loading dataset...")
    train_gen, val_gen, test_gen = trainer.get_data_generators(TRAIN_DIR, VAL_DIR, TEST_DIR)
    
    print(f"  Classes: {len(trainer.class_names)}")
    print(f"  Class names: {', '.join(trainer.class_names[:5])}...")
    
    # Train Model 1: ResNet50
    print("\n1️⃣  Building ResNet50...")
    resnet_model = trainer.build_resnet50()
    print(f"  Model parameters: {resnet_model.count_params():,}")
    resnet_model, resnet_history = trainer.train_model(
        resnet_model, "resnet50", train_gen, val_gen, OUTPUT_DIR
    )
    
    # Train Model 2: EfficientNetB0
    print("\n2️⃣  Building EfficientNetB0...")
    efficientnet_model = trainer.build_efficientnet_b0()
    print(f"  Model parameters: {efficientnet_model.count_params():,}")
    efficientnet_model, efficientnet_history = trainer.train_model(
        efficientnet_model, "efficientnet_b0", train_gen, val_gen, OUTPUT_DIR
    )
    
    # Save class names
    with open(Path(OUTPUT_DIR) / "class_names.pkl", 'wb') as f:
        pickle.dump(trainer.class_names, f)
    
    print("\n" + "="*70)
    print("✓ Training complete!")
    print(f"  Models saved in: {OUTPUT_DIR}")
    print(f"  Next step: Run '3_evaluate_models.py'")
    print("="*70)

if __name__ == "__main__":
    main()
