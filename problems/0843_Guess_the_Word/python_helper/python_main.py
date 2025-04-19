from math import comb

def calc_prob():
    print("Probability of matches:")
    for i in range(7):
        prob = comb(6, i) * (1/26)**i * (25/26)**(6-i)
        print(f"{i} matches: {prob * 100:.2f}%")

def main():
    pass

if __name__ == "__main__":
    calc_prob()
    main()