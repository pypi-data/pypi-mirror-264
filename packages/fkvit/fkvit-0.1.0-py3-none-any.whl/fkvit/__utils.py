import os, time, pkg_resources

animations = [[".(^-^)'", "-(^-^)-", "'(^-^).", "-(^-^)-", ".(^-^)'", "-(^-^)-", "'(^-^).", "-(^-^)-"]]

def path_converter(file_name):
    return pkg_resources.resource_filename('bhagyashree', file_name)

def load_animation(pref="Loading... ", i=0):
    load_str = pref
    ls_len = len(load_str)

    animation = animations[i]
    anicount = 0

    counttime = 0
    i = 0
    count = 0

    while count < 10:
        time.sleep(0.1)

        load_str_list = list(load_str)

        res = ''
        for j in range(ls_len):
            res = res + load_str_list[j]

        print("\r" + res + animation[anicount], end='', flush=True)

        load_str = res

        anicount = (anicount + 1) % 4
        i = (i + 1) % ls_len
        counttime = counttime + 1

        count += 1

    os.system('cls' if os.name == 'nt' else 'clear')