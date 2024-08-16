import tensorflow as tf

# Load the saved_model from the SavedModel format
sub_model = tf.keras.models.load_model('/Users/faroukbelkhyate/Documents/Work/MirrWear/Outfit_Recommendation_Project/saved_model/model_sub')
top_model = tf.keras.models.load_model('/Users/faroukbelkhyate/Documents/Work/MirrWear/Outfit_Recommendation_Project/saved_model/model_top')
bottom_model = tf.keras.models.load_model('/Users/faroukbelkhyate/Documents/Work/MirrWear/Outfit_Recommendation_Project/saved_model/model_bottom')
foot_model = tf.keras.models.load_model('/Users/faroukbelkhyate/Documents/Work/MirrWear/Outfit_Recommendation_Project/saved_model/model_shoes')


# Save the models in the new .keras format
sub_model.save('/Users/faroukbelkhyate/Documents/Work/MirrWear/Outfit_Recommendation_Project/saved_model/model_sub.keras', save_format='keras')
top_model.save('/Users/faroukbelkhyate/Documents/Work/MirrWear/Outfit_Recommendation_Project/saved_model/model_top.keras', save_format='keras')
bottom_model.save('/Users/faroukbelkhyate/Documents/Work/MirrWear/Outfit_Recommendation_Project/saved_model/model_bottom.keras', save_format='keras')
foot_model.save('/Users/faroukbelkhyate/Documents/Work/MirrWear/Outfit_Recommendation_Project/saved_model/model_shoes.keras', save_format='keras')
