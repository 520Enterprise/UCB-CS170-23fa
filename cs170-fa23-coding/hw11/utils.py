import matplotlib.pyplot as plt
import pickle
import time
import tqdm
    
def timing_helper(set_cover_reduction, set_cover_naive):
    with open('data.pkl', 'rb') as f:
        U_all, S_all, ans_all, N_PER_SIZE = pickle.load(f)['q1']

    reduction_times = [0]* (len(U_all)//N_PER_SIZE)
    naive_times = [0]* (len(U_all)//N_PER_SIZE)
    for i, (U, S, ans) in tqdm.tqdm(enumerate(list(zip(U_all, S_all, ans_all)))):
        start = time.time()
        set_cover_reduction(U, S)
        end = time.time()
        reduction_times[i//N_PER_SIZE] += (end - start) / N_PER_SIZE

        start = time.time()
        set_cover_naive(U, S)
        end = time.time()
        naive_times[i//N_PER_SIZE] += (end - start) / N_PER_SIZE

    print(f'Approximate speedup: {sum(naive_times) / sum(reduction_times):.3f}')
    plt.plot(reduction_times)
    plt.plot(naive_times)
    plt.title('Log runtimes vs. problem size')
    plt.xlabel('Number of elements in U')
    plt.ylabel('Runtimes (log seconds)')
    plt.yscale('log')
    plt.legend(['reduction', 'naive'])
    plt.show()
