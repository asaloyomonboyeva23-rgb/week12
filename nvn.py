def process_donations(filename):
    total_donations = {}  
    top_donors = [] 
    with open(filename, "r") as file:
        for line in file :
            line  = line.strip().split(",")
            if len(line) != 4:
                continue
            name , cause , cash_amount , check_amount = line 
            try:
                total =  float(cash_amount) + float(check_amount)
                total_donations[cause] = total_donations.get(cause, 0) + total
                if total > 500: 
                    top_donors.append((name, total))
            except ValueError:
                continue
        return total_donations, top_donors
def write_fundraising_report(cause_totals, top_donors):
    with open("fundraising_summary.txt" , "w") as file:
        file.write("FUNDS RAISED PER CAUSE\n" + "---------------------\n")
        for cause, total in cause_totals.items(): 
            file.write(f"{cause}: ${total:.2f}\n")
        file.write("\nGOLD TIER DONORS (> $500)\n" + "-------------------------\n")
        for name, total in top_donors: 
            file.write(f"{name} (${total:.2f})\n")
cause_totals, top_donors = process_donations("donations.txt") 
write_fundraising_report(cause_totals, top_donors)


                

  
