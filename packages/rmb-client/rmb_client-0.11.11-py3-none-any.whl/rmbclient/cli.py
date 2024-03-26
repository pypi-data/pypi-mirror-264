import argparse
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="Interactive CLI for RMB client.")
    parser.add_argument('-a', '--api_url',
                        type=str,
                        default='https://api.asktable.com',
                        help='The API URL for the RMB client.')
    parser.add_argument('-t', '--token',
                        type=str,
                        default='token1',
                        help='The token for authentication.')

    args = parser.parse_args()

    # 导入 RMB 类
    from rmbclient import RMB
    from rmbclient.exceptions import Unauthorized
    rmb = RMB(token=args.token, api_url=args.api_url)
    print(f"\n-- RMB 客户端({rmb.version})初始化...")
    print("-- 连接服务器(-a)：", args.api_url)
    try:
        t = rmb.token
    except Unauthorized:
        print(f"-- 使用Token (-t)： {args.token} 无效，请检查是否正确。")
        return
    print("-- 使用Token (-t)：", args.token)
    print("-- 您可以使用 'rmb' 来访问RMB，比如：通过 'rmb.datasources' 来查询数据源列表")
    print("   完整的使用方法，请参考帮助文档：https://pypi.org/project/rmb-client/\n")

    try:
        # 尝试导入 IPython
        from IPython import start_ipython
        start_ipython(argv=[], user_ns={'rmb': rmb})
    except ImportError:
        # 如果 IPython 未安装，使用标准 Python shell
        import code
        code.interact(local=locals())


if __name__ == "__main__":
    main()
