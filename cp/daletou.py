import random


def generate_lottery_numbers():
    """
    生成一注大乐透号码
    前区：从1-35中选出5个不重复的号码
    后区：从1-12中选出2个不重复的号码
    """
    # 前区号码
    front_pool = list(range(1, 36))
    front_numbers = sorted(random.sample(front_pool, 5))

    # 后区号码
    back_pool = list(range(1, 13))
    back_numbers = sorted(random.sample(back_pool, 2))

    return front_numbers, back_numbers


def print_lottery_numbers(count=1):
    """
    打印指定数量的大乐透号码
    :param count: 要生成的注数
    """
    print("\n大乐透选号结果：")
    print("=" * 30)
    for i in range(count):
        front, back = generate_lottery_numbers()
        print(f"第{i + 1}注: 前区 {', '.join(map(str, front))} | 后区 {', '.join(map(str, back))}")
    print("=" * 30)
    print("祝您中奖！")


if __name__ == "__main__":
    try:
        num = int(input("请输入要生成的注数(1-10): "))
        if num < 1 or num > 10:
            print("注数应在1-10之间，将默认生成1注")
            num = 1
    except ValueError:
        print("输入无效，将默认生成1注")
        num = 1

    print_lottery_numbers(num)