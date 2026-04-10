import pandas as pd

file_path = "data/UNSW-NB15_1.csv"

# Correct headers
col_names = [
    "srcip","sport","dstip","dsport","proto","state","dur","sbytes","dbytes",
    "sttl","dttl","sloss","dloss","service","Sload","Dload","Spkts","Dpkts",
    "swin","dwin","stcpb","dtcpb","smeansz","dmeansz","trans_depth","res_bdy_len",
    "Sjit","Djit","Stime","Ltime","Sintpkt","Dintpkt","tcprtt","synack","ackdat",
    "is_sm_ips_ports","ct_state_ttl","ct_flw_http_mthd","is_ftp_login","ct_ftp_cmd",
    "ct_srv_src","ct_srv_dst","ct_dst_ltm","ct_src_ltm","ct_src_dport_ltm","ct_dst_sport_ltm",
    "ct_dst_src_ltm","attack_cat","label"
]

# Load dataset
df = pd.read_csv(file_path, names=col_names, skiprows=1, low_memory=False)
print("✅ Dataset loaded. Rows:", len(df))

# Keep useful cols
df = df[["sport","dsport","proto","sbytes","dbytes","dur","attack_cat","label"]]

# Extended port list
common_ports = [21,22,23,25,53,80,110,123,161,389,443,8080,8888]

# === Improved Risk Mapping ===
def assign_risk(row):
    if row["label"] == 0:
        return "Safe"
    attack = str(row.get("attack_cat", "")).lower()
    if "shellcode" in attack or "worms" in attack or "backdoor" in attack:
        return "Critical"
    elif "exploits" in attack or "generic" in attack:
        return "High"
    elif "reconnaissance" in attack or "fuzzers" in attack:
        return "Medium"
    else:
        return "Low"

df["risk_label"] = df.apply(assign_risk, axis=1)

# Port features
for port in common_ports:
    df[f"port_{port}"] = df.apply(
        lambda row: 1 if (row["sport"] == port or row["dsport"] == port) else 0,
        axis=1,
    )

# Extra features
df["bytes_sent"] = df["sbytes"]
df["bytes_recv"] = df["dbytes"]
df["duration"] = df["dur"]

# Final dataset (keep all rows)
final_df = df[[f"port_{p}" for p in common_ports] + ["bytes_sent","bytes_recv","duration","risk_label"]]

# Save full dataset
final_df.to_csv("iot_real_dataset.csv", index=False)
print("✅ Full dataset saved as iot_real_dataset.csv")
print(final_df["risk_label"].value_counts())
