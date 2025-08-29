# Step 3: Create boolean flags like in=a, in=b, in=c
merged_all['in_a'] = merged_all['ab_flag'].isin(['both', 'left_only'])   # from ecmp
merged_all['in_b'] = merged_all['ab_flag'].isin(['both', 'right_only'])  # from portal
merged_all['in_c'] = merged_all['c_flag'].isin(['both', 'right_only'])   # from sor

# Step 4: Apply SAS logic: if (a and c) or (b and c)
mask = ((merged_all['in_a'] & merged_all['in_c']) |
        (merged_all['in_b'] & merged_all['in_c']))
final = merged_all[mask].copy()
