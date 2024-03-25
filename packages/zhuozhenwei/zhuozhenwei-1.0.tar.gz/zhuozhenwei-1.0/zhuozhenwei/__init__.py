def eat():
    print("zzw is eating")


def run():
    print("zzw is running to eat")


def kiss():
    print("zzw is kissing with lzb")


def cry():
    print("zzw is crying")


def angry():
    print("zzw is very angry")


def love():
    print(
        "\n".join(
            [
                "".join(
                    [
                        (
                            "Love"[(x - y) % len("Love")]
                            if ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1) ** 3
                            - (x * 0.05) ** 2 * (y * 0.1) ** 3
                            <= 0
                            else " "
                        )
                        for x in range(-30, 30)
                    ]
                )
                for y in range(30, -30, -1)
            ]
        )
    )
