import dns.resolver

def query_dns(domain, record_type):
    try:
        answers = dns.resolver.resolve(domain, record_type)
        for rdata in answers:
            print(f"{domain} {record_type}: {rdata}")
    except dns.resolver.NXDOMAIN:
        print(f"{domain} not found")
    except dns.resolver.NoAnswer:
        print(f"No {record_type} records found for {domain}")
    except Exception as e:
        print(f"Error querying {domain}: {str(e)}")

# 示例查询
domain = "public_minio"
record_type = "A"  # 可以是A, AAAA, MX, CNAME等

query_dns(domain, record_type)
