import os


# 白名单，避免被误删
WHITELIST = ['pip', 'setuptools']
# 需要删除的模块列表
REMOVELIST = []


def _get_requires(module_name):
    """
    查看一个模块的依赖
    :param module_name: 模块名
    :return: module_name 所依赖的模块的列表
    """
    with os.popen('pip show %s' % module_name) as p:
        requires = p.readlines()
        if not len(requires):
            return []

        reqs = ''
        for line in requires:
            if not line.startswith('Requires:'):
                continue
            reqs = line.strip()
        
        requires = reqs.split(':')[-1].replace(' ', '').strip()
        if requires:
            requires = requires.split(',')
        else:
            requires = []
        return requires


def _get_required_bys(module_name):
    """
    查看一个模块被哪些模块依赖
    :param module_name: 模块名
    :return: module_name 被依赖的模块的列表
    """
    with os.popen('pip show %s' % module_name) as p:
        req_by = p.readlines()
        if not len(req_by):
            return []

        required = ''
        for line in req_by:
            if not line.startswith('Required-by:'):
                continue
            required = line.strip()
        
        req_by = required.split(':')[-1].replace(' ', '').strip()
        if req_by:
            req_by = req_by.split(',')
        else:
            req_by = []
        return req_by


def install(name):
    os.system(f'pip install {name}')


def _get_all_requires(module_name):
    """
    递归地获取一个模块所有的依赖
    :param module_name: 模块名称
    :return: None
    """
    dependents = _get_requires(module_name)
    for package in dependents:
        if package in WHITELIST:
            #print(f'[{package}] in white list')
            continue
        _get_all_requires(package)
    REMOVELIST.append(module_name)


def _remove(module_name):
    print('Scanning packages...')
    _get_all_requires(module_name)
    s_packages =  ','.join(REMOVELIST)
    print(f'[INFO]Found packages: {s_packages}\n')

    for package in REMOVELIST:
        req_bys = _get_required_bys(package)
        print('[INFO]removing:', package)
        #print(package, 'is required by:', req_bys)
        flag = True
        for req_by in req_bys:
            if req_by not in REMOVELIST:
                flag = False
                print(f'[NOTICE]As "{package}" is required by "{req_by}" which is not in {REMOVELIST}, skipped...\n')
                break
        if flag:
            print('\n')
            os.system('pip uninstall -y %s' % package)



# 查看依赖树
def check_tree():
    os.system('pipdeptree.exe')

# 删除依赖包
def remove_pkg():
    pkg_name = input('请输入要卸载的第三方模块包:')
    _remove(pkg_name)



