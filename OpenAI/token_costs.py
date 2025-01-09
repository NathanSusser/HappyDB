# Redefine all values after reset

# Define given token statistics for 50 rows
input_total_tokens_1000 = 23298890  # Total input tokens for 50 rows
output_total_tokens_1000 = 143000  # Total output tokens for 50 rows

# Pricing details for models
pricing_gpt4_api = {"input": 2.50 / 1e6, "cached_input": 1.25 / 1e6, "output": 10.00 / 1e6}
pricing_gpt4_batch = {"input": 1.25 / 1e6, "output": 5.00 / 1e6}
pricing_gpt4_mini_api = {"input": 0.150 / 1e6, "cached_input": 0.075 / 1e6, "output": 0.600 / 1e6}
pricing_gpt4_mini_batch = {"input": 0.075 / 1e6, "output": 0.300 / 1e6}

# Calculate costs for GPT-4 API
cost_gpt4_api_input_50 = pricing_gpt4_api["input"] * input_total_tokens_1000
cost_gpt4_api_output_50 = pricing_gpt4_api["output"] * output_total_tokens_1000
total_gpt4_api_50 = cost_gpt4_api_input_50 + cost_gpt4_api_output_50

# Calculate costs for GPT-4 Batch API
cost_gpt4_batch_input_50 = pricing_gpt4_batch["input"] * input_total_tokens_1000
cost_gpt4_batch_output_50 = pricing_gpt4_batch["output"] * output_total_tokens_1000
total_gpt4_batch_50 = cost_gpt4_batch_input_50 + cost_gpt4_batch_output_50

# Calculate costs for GPT-4 Mini API
cost_gpt4_mini_api_input_50 = pricing_gpt4_mini_api["input"] * input_total_tokens_1000
cost_gpt4_mini_api_output_50 = pricing_gpt4_mini_api["output"] * output_total_tokens_1000
total_gpt4_mini_api_50 = cost_gpt4_mini_api_input_50 + cost_gpt4_mini_api_output_50

# Calculate costs for GPT-4 Mini Batch API
cost_gpt4_mini_batch_input_50 = pricing_gpt4_mini_batch["input"] * input_total_tokens_1000
cost_gpt4_mini_batch_output_50 = pricing_gpt4_mini_batch["output"] * output_total_tokens_1000
total_gpt4_mini_batch_50 = cost_gpt4_mini_batch_input_50 + cost_gpt4_mini_batch_output_50

# Compile results for 50 rows
results_50 = {
    "GPT-4 API (50 rows)": total_gpt4_api_50,
    "GPT-4 Batch API (50 rows)": total_gpt4_batch_50,
    "GPT-4 Mini API (50 rows)": total_gpt4_mini_api_50,
    "GPT-4 Mini Batch API (50 rows)": total_gpt4_mini_batch_50,
}

print(results_50)
