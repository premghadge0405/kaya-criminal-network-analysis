import pandas as pd
import random

# Core entities for our mock criminal network
suspects = ["Rajesh Kumar", "Vikram Singh", "Amit Patel", "Suresh Sharma", "Neha Gupta", "Karan Malhotra"]
locations = ["Connaught Place", "Andheri West", "Koramangala", "Salt Lake", "Banjara Hills"]

# 1. Unstructured FIR Data
firs = []
for i in range(12):
    s1, s2 = random.sample(suspects, 2)
    firs.append({"fir_id": f"FIR-{100+i}", "text": f"Intelligence suggests {s1} met with {s2} near {random.choice(locations)}."})
pd.DataFrame(firs).to_csv("mock_firs.csv", index=False)

# 2. Structured Call Detail Records (CDRs)
calls = []
for i in range(15):
    caller, receiver = random.sample(suspects, 2)
    calls.append({"caller": caller, "receiver": receiver, "duration_sec": random.randint(10, 300)})
pd.DataFrame(calls).to_csv("mock_cdrs.csv", index=False)

# 3. Structured Financial Transactions
txns = []
for i in range(10):
    sender, receiver = random.sample(suspects, 2)
    txns.append({"sender": sender, "receiver": receiver, "amount": random.randint(10000, 500000)})
pd.DataFrame(txns).to_csv("mock_financials.csv", index=False)

print("Success: Generated multi-source datasets (FIRs, CDRs, Financials).")