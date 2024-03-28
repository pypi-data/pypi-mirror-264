import sys
from haretools.pipremove import check_tree,remove_pkg

# 定义菜单选项及对应的操作和说明
menu_items = {
    "0": {"功能函数": exit,         "描述": "退出程序"},
    "1": {"功能函数": check_tree,   "描述": "查看当前依赖树"},
    "2": {"功能函数": remove_pkg,   "描述": "卸载第三方模块包"},
}



def main_menu():
    print("欢迎使用命令行菜单")
    for key, value in menu_items.items():
        print(f"{key}. {value['描述']}")

    choice = input("请输入选项的数字编号: ")

    if choice in menu_items:
        menu_items[choice]['功能函数']()
    else:
        print("无效的选项，请重新输入")
        main_menu(menu_items)


if __name__ == '__main__':
    # 启动菜单
    sys.exit(main_menu())
