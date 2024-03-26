signatures_lv0_exception = {
    'type': 'exception',
    '0000': '''
    Traceback \(most recent call last\)
    '''
}

# 4,5,7少见
signatures_lv0_noexception = {
    'type': 'noexception',
    '0000': '''
    terminate called without an active exception
    ''',
    '0001': '''
    pytorch_lightning.utilities.distributed - INFO - iteration: \d+
    ''',
    '0002': '''
    XpilotLightning: error: unrecognized arguments: [^\n]*\n?
    ''',
    '0003': '''
    100\.0%
    ''',
    '0004': '''
    loading dataloader.*
    ''',
    '0005': '''
    text norm: \d+ lines done.
    ''',
    '0006': '''
    All [a-zA-Z]+ processes registered. Starting( ddp)? with \d+ processes
    ''',
    '0007': '''
    Model at rank \d+ finished transferring to ddp
    ''',
    '0008': '''
    error: unrecognized arguments
    ''',
    '0009': '''
    error: the following arguments are required
    ''',
    '0010': '''
    syntax error 
    ''',
    '0011': '''
    error: argument [\w\/\-_]*: expected [^^\n]* 
    '''

}

signatures_lv1_dataloader = {
    'type': 'dataloader',
    '0000': '''
    ValueError: `Dataloader` returned 0 length. Please make sure that it returns at least 1 batch
    ''',
    '0001': '''
    xpilot_lightning.exceptions.exceptions.DataloaderException: LID Dataset init error: [^\n]*\n?
    ''',
    '0002': '''
    xpilot_lightning.exceptions.exceptions.DataloaderException: Dataset error: [^\n]*\n?
    ''',
    '0003': '''
    RuntimeError: Error\(s\) in loading state_dict for \w+?:
    ''',
    '004': '''
    RuntimeError: stack expects each tensor to be equal size 
    ''',
    '0005': '''
    sqlite3.OperationalError: [^\n]*\n?
    ''',
    '0006': '''
    xpilot_lightning.exceptions.exceptions.DataloaderException: Caught DataloaderException in DataLoader worker process \d+\n?
    ''',
    '0007': '''
    xpilot_lightning.exceptions.exceptions.DataloaderException\n?
    ''',
    '0008': '''
    xpilot_lightning.exceptions.exceptions.DatasetException: [^\n]*\n?
    '''

}

signatures_lv1_usercode = {
    'type': 'usercode',
    '0000': '''
    FileNotFoundError: [^\n]*\n?
    ''',
    '0001': '''
    ModuleNotFoundError: [^\n]*\n?
    ''',
    '0002': '''
    TypeError: [^\n]*\n?
    ''',
    '0003': '''
    OSError: [^\n]*\n?
    ''',
    '0004': '''
    ZeroDivisionError: [^\n]*\n?
    ''',
    '0005': '''
    pytorch_lightning.utilities.exceptions.MisconfigurationException: [^\n]*\n?
    ''',
    '0006': '''
    AssertionError: [^\n]*\n?
    ''',
    '0007': '''
    IndentationError: [^\n]*\n?
    ''',
    '0008': '''
    KeyError: '\w+?'
    ''',
    '0009': '''
    AttributeError: [^\n]*\n?
    ''',
    '0010': '''
    IndexError: [^\n]*\n?
    ''',
    '0011': '''
    ValueError: [^`][^\n`]*\n?
    ''',
    '0012': '''
    UnboundLocalError: [^\n]*\n?
    ''',
    '0013': '''
    NameError: name '\w+?' is not defined
    ''',
    '0014': '''
    ImportError: [^\n]*\n?
    ''',

    '0015': '''
    yaml.parser.ParserError: [^\n]*\n?
    ''',
    '0016': '''
    json.decoder.JSONDecodeError: [^\n]*\n?
    ''',
    '0017': '''
    XpilotLightning: error: argument [^\n]*\n?
    ''',
    '0018': '''
    pytorch_lightning.utilities.exceptions.DeadlockDetectedException: DeadLock detected from rank: \d+
    ''',
    '0019': '''
    RuntimeError: The size of tensor a \(\d+\) must match the size of tensor b \(\d+\) at non-singleton dimension \d
    ''',
    '0020': '''
    SyntaxError: invalid syntax
    ''',
    '0021': '''
    FileExistsError: [^\n]*\n?
    ''',
    '0022': '''
    assert [^\n]*\n
    ''',
    '0023': '''
    RuntimeError: Sizes of tensors must match except in dimension \d+
    ''',
    '0024': '''
    RuntimeError: [a-zA-Z0-0\-_']* directory does not exist.
    ''',
    '0025': '''
    AssertionError(: )?[^\n]*\n?
    ''',
    '0026': '''
    NotImplementedError: [^\n]*\n?
    ''',
    '0027': '''
    NotImplementedError\n
    ''',
    '0028': '''
    No such file or directory
    ''',
    '0029': '''
    yaml.scanner.ScannerError: [^\n]*\n?
    ''',
    '0030': '''
    \[FATAL tini \(\d+\)\] [^\n]*\n?
    ''',
    '0031': '''
    python: can't open file [^\n]*\n?
    ''',

    '0032': '''
    AssertionError
    ''',

    '0099': '''
    RuntimeError(: )?[^\n]*\n?
    '''

}

signatures_lv1_cuda = {
    'type': 'cuda',
    '0000': '''
    RuntimeError: CUDA( error: CUDA)? out of memory
    ''',
    '0001': '''
    RuntimeError: CUDA error: an illegal memory access was encountered
    ''',
    '0002': '''
    RuntimeError: CUDA error: unspecified launch failure
    ''',
    '0003': '''
    RuntimeError: CUDA error: uncorrectable ECC error encountered
    ''',
    '0004': '''
    RuntimeError: NCCL error in: [^\n]*\n?
    ''',
    '0005': '''
    RuntimeError: CUDA error: initialization error [^\n]*\n?
    ''',
    '0006': '''
    RuntimeError: CUDA error: uncorrectable NVLink error detected during the execution
    ''',
    #  7 可以包含上面大部分
    '0007': '''
    RuntimeError: CUDA error: [^\n]*\n?
    ''',

    '0008': '''
    torch.cuda.OutOfMemoryError: CUDA out of memory
    '''

}

signatures_lv1_infra = {
    'type': 'infra',
    '0000': '''
    RuntimeError: Timed out initializing process group in store based barrier on rank [^\n]*\n?
    ''',
    '0002': '''
    xpilot_lightning.exceptions.exceptions.WandBException: [^\n]*\n?
    ''',
    '0003': '''
    Connection(Reset|Refused)Error: \[Errno \d+\] [^\n]*\n?
    ''',
    '0004': '''
    BrokenPipeError: \[Errno \d+\] [^\n]*\n?
    ''',
    '0005': '''
    RuntimeError: Connection reset by peer
    ''',
    # wandb: ERROR Error uploading [^\n]*\n        wandb: ERROR Error while calling W&B API: [^\n]*\n?
    # wandb: ERROR Internal wandb error:            wandb: ERROR api_key not configured
    # data/bifrost-20221229214540-zhangc6-0.err.log  wandb error， 但是有all dpp process registered.
    '0006': '''
    wandb: ERROR [^\n]*\n?
    ''',
    '0007': '''
    xpilot_lightning.exceptions.exceptions.WandBException: [^\n]*\n?
    ''',

}

# RuntimeError: Default process group has not been initialized, please make sure to call init_process_group
# ProcessLookupError: [Errno 3] No such process     这个通常是由其他引起，在它之前会有其他错误
# _pickle.UnpicklingError: pickle data was truncated

# RuntimeError: cuDNN error ->  CUDA OOM

worker_process_exception = {
    'type': 'worker_process',
    '0000': '''
    Load dataset completed
    ''',
    '0001': '''
    xpilot_lightning.exceptions.exceptions.DataloaderException: Caught DataloaderException in DataLoader worker process \d+\n?
    ''',
}
