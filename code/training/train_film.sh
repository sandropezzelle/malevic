
#!/usr/bin/env bash

"""

This script will train FiLM using pre-trained ResNet101 features for:
 4 tasks: a, b, c, d
 3 runs: 1 2 3
 4 learning rates: 5e-5, 5e-4, 5e-3, 3e-4
 2 dropout values: 0, 0.5
 2 classifier batchnorm values: 0, 1
and will save all models in './saved_models/film/'

"""

# Optional:
# Activate your virtual environment with pytorch1.0 and python3.5
#. /myvirtualenv/bin/activate


for el in 'a' 'b_vague' 'c_vague' 'd_vague'
do
   echo "Running task $el"
   for lr in '5e-4' '3e-4' '5e-5' '5e-3'
do
       echo "Learning rate equal to $lr"
       for dr in '0' '0.5'
do
          echo "Dropout equal to $dr"
          for bn in '0' '1'
do
             echo "Batch normalization $bn"
             for i in 1 2 3
do
                echo "Running $i times"
                for m in 'film'
do
                   echo "Running $m architecture"
                   
                   python scripts/train_model.py \
                     --model_type FiLM \
                     --train_question_h5 ../data/${el}_dataset/train_questions.h5 \
                     --train_features_h5 ../data/${el}_dataset/visual_features/train_features.h5 \
                     --val_question_h5 ../data/${el}_dataset/val_questions.h5 \
                     --val_features_h5 ../data/${el}_dataset/visual_features/val_features.h5 \
                     --vocab_json  ../data/${el}_dataset/vocab.json \
                     --num_train_samples 16000 \
                     --num_val_samples 2000 \
                     --classifier_dropout ${dr} \
                     --classifier_batchnorm ${bn} \
                     --learning_rate ${lr} \
                     --feature_dim 1024,14,14 \
                     --batch_size 64 \
                     --num_iterations 10000 \
                     --record_loss_every 1 \
                     --checkpoint_every 250 \
                     --use_coords 1 \
                     --module_stem_batchnorm 1 \
                     --bidirectional 0 \
                     --decoder_type linear \
                     --encoder_type gru \
                     --module_stem_num_layers 1 \
                     --module_batchnorm 1 \
                     --weight_decay 1e-5 \
                     --rnn_num_layers 1 \
                     --rnn_wordvec_dim 200 \
                     --rnn_hidden_dim 4096 \
                     --rnn_output_batchnorm 0 \
                     --classifier_downsample maxpoolfull \
                     --classifier_proj_dim 512 \
                     --classifier_fc_dims 1024 \
                     --module_input_proj 1 \
                     --module_residual 1 \
                     --module_dim 128 \
                     --module_kernel_size 3 \
                     --module_batchnorm_affine 0 \
                     --module_num_layers 1 \
                     --num_modules 4 \
                     --module_dropout 0e-2 \
                     --condition_pattern 1,1,1,1 \
                     --gamma_option linear \
                     --gamma_baseline 1 \
                     --use_gamma 1 \
                     --use_beta 1 \
                     --checkpoint_path ./saved_models/film/${el}_${m}_drop${dr}_bn${bn}_lr${lr}_run${i}.pt

done
done
done
done
done
done
