
#!/usr/bin/env bash

"""

This script will train CNN+LSTM and CNN+LSTM+SA using pre-trained ResNet101 features for:
 4 tasks: a, b, c, d
 3 runs: 1 2 3
 4 learning rates: 5e-3, 5e-4, 5e-5, 3e-4
 2 dropout values: 0, 0.5
 2 classifier batchnorm values: 0, 1
and will save all models in './saved_models/baselines/'

"""

# Optional:
# Activate your virtual environment with pytorch1.0 and python3.5
#. /myvirtualenv/bin/activate

for el in 'a' 'b_vague' 'c_vague' 'd_vague'
do
   echo "Running task $el"
   for lr in '5e-3' '5e-4' '5e-5' '3e-4'
do
       echo "Learning rate equal to $lr"
       for dr in '0.5' '0'
do
          echo "Dropout equal to $dr"
          for bn in '1' '0'
do
             echo "Batch normalization $bn"
             for m in 'CNN+LSTM' 'CNN+LSTM+SA'
do
                echo "Running $m architecture"
                for i in 1 2 3
do
                   echo "Running $i times"
                   python scripts/train_model.py \
                     --model_type ${m} \
                     --train_question_h5 ../data/${el}_dataset/train_questions.h5 \
                     --train_features_h5 ../data/${el}_dataset/visual_features/train_features.h5 \
                     --val_question_h5 ../data/${el}_dataset/val_questions.h5 \
                     --val_features_h5 ../data/${el}_dataset/visual_features/val_features.h5 \
                     --vocab_json  ../data/${el}_dataset/vocab.json \
                     --num_train_samples 16000 \
                     --num_val_samples 2000 \
                     --feature_dim 1024,14,14 \
                     --batch_size 64 \
                     --num_iterations 10000 \
                     --record_loss_every 1 \
                     --checkpoint_every 250 \
                     --classifier_fc_dims 1024 \
                     --classifier_dropout ${dr} \
                     --classifier_batchnorm ${bn} \
                     --learning_rate ${lr} \
                     --checkpoint_path ../saved_models/baselines/${el}_${m}_drop${dr}_bn${bn}_lr${lr}_run${i}.pt

done
done
done
done
done
done