import hashlib
import itertools
import string
import time
from multiprocessing import Pool, cpu_count, Value
import os # 导入os模块用于获取进程ID，方便调试

# 全局共享变量用于在不同进程间指示是否找到密码
found_password = Value('b', False) # 'b' 表示布尔类型

def generate_and_check(args):
    """
    生成一个范围内的所有可能字符串，并检查其MD5哈希值是否与目标匹配。
    这个函数会被多个进程并行调用。
    """
    global found_password
    target_md5_hash, chars, password_length, start_char_idx_range = args

    start_idx, end_idx = start_char_idx_range # 解包范围

    start_time_process = time.time()
    
    # 如果其他进程已经找到密码，则当前进程可以提前退出
    if found_password.value:
        return None

    # 遍历分配给当前进程的第一个字符的索引范围
    for first_char_index in range(start_idx, end_idx):
        if found_password.value: # 每次内层循环前检查全局标志
            break
        
        first_char = chars[first_char_index]

        # 如果密码长度为1，直接检查第一个字符
        if password_length == 1:
            candidate_password = first_char
            md5_calculated = hashlib.md5(candidate_password.encode('utf-8')).hexdigest()
            if md5_calculated == target_md5_hash:
                with found_password.get_lock():
                    if not found_password.value:
                        found_password.value = True
                        print(f"\n***** 成功找到匹配项！ *****")
                        print(f"目标MD5哈希值: {target_md5_hash}")
                        print(f"原始明文可能是: '{candidate_password}'")
                        print(f"进程 {os.getpid()} (处理 '{first_char}' 开始的范围) 完成时间: {time.time() - start_time_process:.2f} 秒")
                        return candidate_password
        else:
            # 生成剩余长度的字符排列
            for permutation_suffix in itertools.product(chars, repeat=password_length - 1):
                if found_password.value: # 每次内层循环前检查全局标志
                    break
                
                candidate_password = first_char + "".join(permutation_suffix)
                
                md5_calculated = hashlib.md5(candidate_password.encode('utf-8')).hexdigest()

                if md5_calculated == target_md5_hash:
                    with found_password.get_lock(): # Acquire lock before modifying shared variable
                        if not found_password.value: # Double-check to prevent multiple writes
                            found_password.value = True
                            print(f"\n***** 成功找到匹配项！ *****") 
                            print(f"目标MD5哈希值: {target_md5_hash}") #b5c0b187fe309af0f4d35982fd961d7e
                            print(f"原始明文可能是: '{candidate_password}'")
                            print(f"进程 {os.getpid()} (处理 '{first_char}' 开始的范围) 完成时间: {time.time() - start_time_process:.2f} 秒")
                            return candidate_password # Return the found password

    return None # Password not found by this process within its assigned range

def main():
    target_hash = input("请输入您想要暴力破解的MD5哈希值: ").strip().lower()

    min_length = int(input("请输入要尝试的最小密码长度 (建议小值，如 1): "))
    max_length = int(input("请输入要尝试的最大密码长度 (建议小值，如 1-7): "))

    if min_length > max_length or min_length < 0:
        print("错误：最小长度不能大于最大长度，且必须为非负数。")
        return

    # 包含所有可能的字符
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation # 所有可见字符
    #chars = string.ascii_lowercase # 仅小写字母
    #chars = string.digits # 仅数字
    print(f"使用的字符集: {chars}")
    print(f"字符集大小: {len(chars)}")

    num_processes = cpu_count()
    print(f"检测到 {num_processes} 个CPU核心，将使用 {num_processes} 个进程。")

    start_time = time.time()

    # 迭代尝试不同的密码长度范围
    for length in range(min_length, max_length + 1):
        if found_password.value: # 如果已经找到密码，则提前退出
            break

        print(f"\n正在尝试破解长度为 {length} 的密码...")

        if length == 0: # 处理空字符串的情况
            if target_hash == hashlib.md5("".encode('utf-8')).hexdigest():
                with found_password.get_lock():
                    if not found_password.value:
                        found_password.value = True
                        print(f"\n***** 成功找到匹配项！ *****")
                        print(f"目标MD5哈希值: {target_hash}")
                        print(f"原始明文可能是: '' (空字符串)")
                        return # 退出主程序

        # 分配任务给每个进程
        # 每个进程负责处理 `chars` 列表中一部分作为第一个字符的组合
        # 注意：如果 length == 0，下面的分配逻辑不适用，已在上面单独处理
        
        # 确保每个进程至少分到一部分字符，或者全部字符如果不够分
        if len(chars) < num_processes: # 如果字符集比核心数少，则每个核心处理一个或多个字符
            chunk_size = 1
        else:
            chunk_size = len(chars) // num_processes # 每个进程至少分到的字符数

        tasks = []
        for i in range(num_processes):
            start_idx = i * chunk_size
            end_idx = (i + 1) * chunk_size
            if i == num_processes - 1: # 确保最后一个进程处理所有剩余的字符
                end_idx = len(chars)
            
            # 如果某个 chunk 为空，则跳过
            if start_idx >= len(chars):
                continue
            
            # 传递一个元组作为第一个字符索引的范围
            tasks.append((target_hash, chars, length, (start_idx, end_idx)))
        
        if not tasks and length > 0: # 如果chars为空且length>0，或者任务分配失败
            print(f"警告：对于长度 {length}，没有有效的字符范围可以分配给进程。请检查字符集或长度设置。")
            continue

        with Pool(num_processes) as pool:
            # map 将迭代地把 tasks 中的每个元素传递给 generate_and_check 函数
            async_results = [pool.apply_async(generate_and_check, (task,)) for task in tasks]

            # 等待结果，并检查是否找到密码
            for res in async_results:
                try:
                    result = res.get() # 等待每个子进程完成并获取结果
                    if result: # 如果任何一个进程找到了密码
                        print(f"总耗时: {time.time() - start_time:.2f} 秒")
                        pool.terminate() # 立即停止所有其他进程
                        return # 退出主程序
                except Exception as e:
                    print(f"子进程发生错误: {e}")
            
            # 如果本轮长度尝试完毕但未找到，检查全局标志是否被其他线程设置
            if found_password.value:
                print(f"总耗时: {time.time() - start_time:.2f} 秒")
                return


    if not found_password.value:
        print(f"\n在尝试所有长度从 {min_length} 到 {max_length} 的组合后，未找到匹配项。")
        print(f"总耗时: {time.time() - start_time:.2f} 秒")

if __name__ == "__main__":
    main()