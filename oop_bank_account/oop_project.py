from bank_accounts import *

Gabri = BankAccount(1000, "Gabri")
Emma = BankAccount(2000, "Emma")

Gabri.getBalance()
Emma.getBalance()

Gabri.deposit(1000)

Emma.withdraw(10000)
Emma.withdraw(100)

Gabri.transfer(1000, Emma)
Emma.transfer(250, Gabri)

Davide = InterestRewardsAcct(1000, "Davide")

Davide.getBalance()
Davide.deposit(100)
Davide.transfer(100, Gabri)

Peco = SavingsAcct(1000, "Peco")

Peco.getBalance()
Peco.deposit(100)
Peco.transfer(1000, Emma)