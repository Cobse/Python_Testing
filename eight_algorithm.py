

def find_eight_eights_1000():
    """
    Finds a combination of exactly eight '8' digits using only addition
    to sum up to 1000.
    
    c3 = count of 888, c2 = count of 88, c1 = count of 8
    
    Constraints:
    1. 3*c3 + 2*c2 + 1*c1 = 8 (Total '8' digits)
    2. 888*c3 + 88*c2 + 8*c1 = 1000 (Total sum)
    """
    solutions = []
    
    # c3 (count of 888) can only be 0 or 1
    for c3 in range(2):
        # c2 (count of 88) can be at most 4
        for c2 in range(5):
            c1_digits_used = 3 * c3 + 2 * c2

            if c1_digits_used > 8:
                continue

            # Calculate c1 required for the digit count to be exactly 8
            c1 = 8 - c1_digits_used

            # Check if this combination sums to 1000
            total_sum = 888 * c3 + 88 * c2 + 8 * c1

            if total_sum == 1000:
                solution = {'888': c3, '88': c2, '8': c1}
                solutions.append(solution)
                # Found the only solution, can return immediately
                return solutions 

    return solutions

if __name__ == "__main__":
    result = find_eight_eights_1000()
    for sol in result:
        print(f"Solution found: 888 used {sol['888']} times, 88 used {sol['88']} times, 8 used {sol['8']} times.\nSum: {888 * sol['888'] + 88 * sol['88'] + 8 * sol['8']}")
