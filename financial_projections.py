'''
Just a simple script to help students with estimating how much student
loan they need.

This is a very simplistic financial projection tool that factors in
your previous spending habits so that you can work out how much money
to save, how much loan to take out, and how much money you can expect
to be left with at the end of year. It uses Monte-Carlo simulations.

The predictions from this should NOT be taken for sound financial advice.
There are several simplifications:
    - Interest is calculated weekly, not monthly.
    - The weekly spendings and interest accrued on stocks and shares are
      are assumed to be normally distributed.
    - The annual income is assumed to be added to the savings account every
      week rather than in termly chunks as the student loan often comes in.

However, I hope that this tool can come in handy for students to plan their
budgeting, and especially to assess different approaches to spending and
saving.
'''

### Imports ###
import datetime
import numpy as np
import matplotlib.pyplot as plt

### Functions ###
def main():
    ''' The main function. '''
    # Number of simulations
    n = 1000
    simulate(n)

def simulate(n):
    ''' Does n simulations and plots the results. '''
    ### Simulation settings - Edit the variables below! ###

    ### Current account and savings account ###
    # The total balance you have in your current accounts now.
    current_account_balance_now = 100
    # The total balance you have in your savings accounts now.
    savings_account_balance_now = 1000
    # The interest you are gaining on the savings.
    savings_account_interest = 4

    ### ISA ###
    # The total balance on your ISA (if applicable).
    isa_balance_now = 1000
    # The mean and standard deviation of the growth rate of your ISA.
    # If you have a stocks and shares ISA, you can go off previous
    # performance to create an estimate for this.
    # If you have a cash ISA, your isa_stdev will be 0.
    isa_stdev = 12
    isa_mean = 8
    # The amount (in pounds) you are putting into your ISA every week.
    isa_weekly_payment = 10

    ### LISA ###
    # The total balance on your LISA (if applicable).
    lisa_balance_now = 1000
    # The mean and standard deviation of the growth rate of your LISA.
    # If you have a stocks and shares LISA, you can go off previous
    # performance to create an estimate for this.
    # If you have a cash LISA, your isa_stdev will be 0.
    lisa_stdev = 8
    lisa_mean = 4
    # The amount (in pounds) you are putting into your LISA every week.
    lisa_weekly_payment = 10

    ### Spendings and Income ###
    # The average amount you spend weekly and standard deviation EXCLUDING
    # ISA and LISA payments.
    # Inputting a higher standard deviation gives you a safer estimate
    # for how much student loan you may wish to take out.
    weekly_spendings_mean = 300
    weekly_spendings_stdev = 100
    # This is your annual income. Add your student loan, earnings
    # from part-time work, and any additional income you may get
    # to this variable.
    annual_inflow = (10000 # Student Loan
                    +100*30 # Part-time Income (i.e. maybe getting £100/week
                            # for 30 weeks)
                    +3000)  # Summer work

    ### Time setting ###
    # The number of weeks you wish to project into the future.
    # Note that this cannot be a float. If you wish to project
    # one year into the future for instance, simply take n_weeks = 52.
    n_weeks = 52
    time_now = datetime.datetime.now()
    date_initial = time_now.strftime("%d/%m/%Y")
    time_final = time_now + datetime.timedelta(days=7*n_weeks)
    date_final = time_final.strftime("%d/%m/%Y")

    # Runs n single simulations and saves the weekly data to lists
    # for the current account, savings account, ISA and LISA.
    savings_account_results = []
    current_account_results = []
    isa_results = []
    lisa_results = []
    for i in range(n):
        sim_results = run_single_simulation(current_account_balance_now=current_account_balance_now,
                        savings_account_balance_now=savings_account_balance_now,
                        savings_account_interest=savings_account_interest,
                        isa_balance_now=isa_balance_now,
                        isa_stdev=isa_stdev,
                        isa_mean=isa_mean,
                        isa_weekly_payment=isa_weekly_payment,
                        lisa_balance_now=lisa_balance_now,
                        lisa_stdev=lisa_stdev,
                        lisa_mean=lisa_mean,
                        lisa_weekly_payment=lisa_weekly_payment,
                        weekly_spendings_mean=weekly_spendings_mean,
                        weekly_spendings_stdev=weekly_spendings_stdev,
                        annual_inflow=annual_inflow,
                        n_weeks=n_weeks)
        savings_account_results.append(sim_results['savings_account'])
        current_account_results.append(sim_results['current_account'])
        isa_results.append(sim_results['isa'])
        lisa_results.append(sim_results['lisa'])

    ### Plots ###
    # Time series plot, showing all n simulations showing balance against time.
    fig, ax = plt.subplots()
    for i in range(n):
        if i == 0:
            ax.plot(np.arange(0, n_weeks, 1), savings_account_results[i], color='red', label='Savings Account')
            ax.plot(np.arange(0, n_weeks, 1), current_account_results[i], color='blue', label='Current Account')
            ax.plot(np.arange(0, n_weeks, 1), isa_results[i], color='green', label='ISA')
            ax.plot(np.arange(0, n_weeks, 1), lisa_results[i], color='orange', label='LISA')
        else:
            ax.plot(np.arange(0, n_weeks, 1), savings_account_results[i], color='red')
            ax.plot(np.arange(0, n_weeks, 1), current_account_results[i], color='blue')
            ax.plot(np.arange(0, n_weeks, 1), isa_results[i], color='green')
            ax.plot(np.arange(0, n_weeks, 1), lisa_results[i], color='orange')
    fig.legend(ncols=4, loc='upper center', bbox_to_anchor=(0.5, 0.95))
    fig.suptitle(f'Financial projection ({date_initial} - {date_final})')
    ax.set_xlabel('Time (weeks)')
    ax.set_ylabel('Balance (£)')
    plt.show()
    plt.close()

    # Histograms, showing the final balance values for all n simulations for
    # each account.
    savings_account_final = [i[-1] for i in savings_account_results]
    current_account_final = [i[-1] for i in current_account_results]
    current_and_savings_final = [savings_account_final[i]+current_account_final[i] for i in range(n)]
    isa_final = [i[-1] for i in isa_results]
    lisa_final = [i[-1] for i in lisa_results]
    total_final = np.array([savings_account_final[i]+current_account_final[i]+isa_final[i]+lisa_final[i] for i in range(n)])

    # Final Current Account balance histogram
    fig, ax = plt.subplots()
    ax.hist(current_and_savings_final, bins=int(n**0.33))
    # Probability of ending up lower than last year (total balance)
    current_and_savings_final = np.array(current_and_savings_final)
    p_lower = len(current_and_savings_final[current_and_savings_final<0])/n * 100
    fig.suptitle(fr'Mean Current+Savings Balance at {date_final} is £{np.mean(current_and_savings_final):.0f} $\pm$ £{np.std(current_and_savings_final):.0f}'\
                 f'\nProbability of Current+Savings Balance below 0 is {p_lower:.1f}%')
    ax.set_xlabel('Balance (£)')
    ax.set_ylabel('Frequency')
    plt.show()
    plt.close()

    # Final ISA Account balance histogram
    fig, ax = plt.subplots()
    ax.hist(isa_final, bins=int(n**0.33))
    fig.suptitle(fr'Mean ISA Balance at {date_final} is £{np.mean(isa_final):.0f} $\pm$ £{np.std(isa_final):.0f}')
    ax.set_xlabel('Balance (£)')
    ax.set_ylabel('Frequency')
    plt.show()
    plt.close()

    # Final LISA Account balance histogram
    fig, ax = plt.subplots()
    ax.hist(lisa_final, bins=int(n**0.33))
    fig.suptitle(fr'Mean LISA Balance at {date_final} is £{np.mean(lisa_final):.0f} $\pm$ £{np.std(lisa_final):.0f}')
    ax.set_xlabel('Balance (£)')
    ax.set_ylabel('Frequency')
    plt.show()

    # Final total balance of all accounts histogram
    fig, ax = plt.subplots()
    ax.hist(total_final, bins=int(n**0.33))
    # Probability of ending up lower than last year (total balance)
    total_start = current_account_balance_now+savings_account_balance_now+isa_balance_now+lisa_balance_now
    p_lower = len(total_final[total_final<total_start])/n * 100
    ax.axvline(x=current_account_balance_now+savings_account_balance_now+isa_balance_now+lisa_balance_now, 
               linestyle='--', label=f'Initial Total Balance (£{total_start:.0f}) at {date_initial}: p(total final < total initial)={p_lower:.1f}%', 
               color='black')
    ax.axvline(x=np.mean(total_final), linestyle='--', color='red',
               label=f'Mean Total Balance at {date_final}: difference is £{np.mean(total_final)-total_start:.0f} $\pm$ £{np.std(total_final):.0f}')
    fig.suptitle(fr'Mean Total Balance at {date_final} is £{np.mean(total_final):.0f} $\pm$ £{np.std(total_final):.0f}')
    fig.legend(loc='upper center', bbox_to_anchor=(0.5, 0.95))
    ax.set_xlabel('Balance (£)')
    ax.set_ylabel('Frequency')
    plt.subplots_adjust(top=0.8)
    plt.show()


def run_single_simulation(current_account_balance_now,
                        savings_account_balance_now,
                        savings_account_interest,
                        lisa_balance_now,
                        isa_balance_now,
                        isa_weekly_payment,
                        isa_stdev,
                        isa_mean,
                        lisa_stdev,
                        lisa_mean,
                        lisa_weekly_payment,
                        weekly_spendings_mean,
                        weekly_spendings_stdev,
                        annual_inflow,
                        n_weeks):
    ''' Runs a single simple Monte-Carlo simulation. '''

    # Initialise lists
    lisa = [0]*n_weeks
    savings_account = [0]*n_weeks
    current_account = [0]*n_weeks
    isa = [0]*n_weeks
    # Set the balance at the beginning of Week 0 to the current values
    # for the balance of the LISA, ISA, Current Account and Savings Account
    lisa[0] = lisa_balance_now
    savings_account[0] = savings_account_balance_now
    current_account[0] = current_account_balance_now
    isa[0] = isa_balance_now

    # Run the Monte-Carlo Simulation
    # Iterate over number of weeks
    for week in range(1, n_weeks):

        ### Savings Account ###
        # Step 1: Add 1/52th of the annual income
        # Step 2: Take away weekly spendings which we assume 
        # are normally distributed.
        # Step 3: Apply interest.
        # These steps are reflected below.
        savings_account[week] = (savings_account[week-1]
                            + annual_inflow/52
                            - np.random.normal(loc=weekly_spendings_mean,
                                            scale=weekly_spendings_stdev))
        savings_account[week] += (savings_account[week] 
                                  * (savings_account_interest/100) 
                                  / 52)

        ### Current Account ###
        # Assume that the balance in the current account 
        # remains roughly constant.
        current_account[week] = current_account[week-1]

        ### ISA ###
        # Step 1: Add injected cash.
        # Step 2: Apply interest which is normally distributed.
        isa[week] = isa[week-1] + isa_weekly_payment
        isa[week] += isa[week] * np.random.normal(loc=(isa_mean/100) / 52,
                                            scale=(isa_stdev/100) / np.sqrt(52))
        ### LISA ###
        # Step 1: Add 125% injected cash since 25% is provided by the government.
        # Step 2: Apply interest which is normally distributed.
        lisa[week] = lisa[week-1] + lisa_weekly_payment*1.25
        lisa[week] += lisa[week] * np.random.normal(loc=(lisa_mean/100) / 52,
                                            scale=(lisa_stdev/100) / np.sqrt(52))

    # Return a dictionary with values showing 
    # the weekly balances of each account.
    return {'savings_account':savings_account, 
            'current_account':current_account, 
            'lisa':lisa, 
            'isa': isa}
if __name__ == '__main__':
    main()