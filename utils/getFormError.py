def getError(form):
    """
        获取form错误文本
    """
    error_list = []
    for item in form.errors:
        error_list.append(form.errors[item][0])
    err_str = '/'.join(error_list)
    return err_str
