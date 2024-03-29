schedulers = {}

schedulers["constant"] = """
lr_scheduler_name: LambdaLR
lr_scheduler_func: pymlip.lrlambda.constant_value
lambda_lr_warm_length: 10
"""

schedulers["linear"] = """
lr_scheduler_name: LambdaLR
lr_scheduler_func: pymlip.lrlambda.linear_sweep
lambda_lr_length: 1000
lambda_lr_warm_length: 10
"""

schedulers["exp05"] = """
lr_scheduler_name: LambdaLR
lr_scheduler_func: pymlip.lrlambda.exp_sweep
lambda_lr_length: 1000
lambda_lr_order: 0.5
lambda_lr_warm_length: 10
"""

schedulers["cos-g99"] = """
lr_scheduler_name: LambdaLR
lr_scheduler_func: pymlip.lrlambda.cos_sweep
lambda_lr_length: 50
lambda_lr_warm_length: 10
lambda_lr_gamma: 0.99
"""

schedulers["cos-g995"] = """
lr_scheduler_name: LambdaLR
lr_scheduler_func: pymlip.lrlambda.cos_sweep
lambda_lr_length: 50
lambda_lr_warm_length: 10
lambda_lr_gamma: 0.995
"""

schedulers["step9-50"] = """
lr_scheduler_name: LambdaLR
lr_scheduler_func: pymlip.lrlambda.step_down
lambda_lr_length: 50
lambda_lr_warm_length: 10
lambda_lr_step_factor: 0.9
"""

schedulers["plateau-25"] = """
lr_scheduler_name: ReduceLROnPlateau
lr_scheduler_patience: 25
lr_scheduler_factor: 0.5
"""

schedulers["plateau-50"] = """
lr_scheduler_name: ReduceLROnPlateau
lr_scheduler_patience: 50
lr_scheduler_factor: 0.5
"""

schedulers["plateau-100"] = """
lr_scheduler_name: ReduceLROnPlateau
lr_scheduler_patience: 100
lr_scheduler_factor: 0.5
"""

schedulers["cosine-warm-50"] = """
lr_scheduler_name: CosineAnnealingWarmRestarts
lr_scheduler_T_0: 50
lr_scheduler_T_mult: 1
lr_scheduler_eta_min: 0.0001
lr_scheduler_last_epoch: -1
"""