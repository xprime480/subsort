import sys
import splitutils

def retr(item_count, target_count, target_buckets, total_buckets) :
    ratio_lo = 0.00001
    ratio_hi = 30.0
    iterations = 0

    while True and iterations < 40 :
        iterations += 1
        ratio = (ratio_lo + ratio_hi) / 2

        tier_counts = splitutils.make_geometric_series(item_count, total_buckets, 1, ratio=ratio)
        #print('trace = {}; {}'.format(ratio, tier_counts))
        total = sum(tier_counts[:target_buckets])
        if total == target_count :
            break
        if total > target_count : 
            ratio_lo = ratio
        else :
            ratio_hi = ratio

    print('tier_ratio = {}'.format(ratio))

if __name__ == '__main__' :
    arg_count = len(sys.argv)

    item_count = 1000
    target_count = 300
    target_buckets = 2
    total_buckets = 10

    if arg_count > 1 :
        item_count = int(sys.argv[1])
    if arg_count > 2 :
        target_count = int(sys.argv[2])
    if arg_count > 3 :
        target_buckets = int(sys.argv[3])
    if arg_count > 4 :
        total_buckets = int(sys.argv[4])

    retr(item_count, target_count, target_buckets, total_buckets)
