import argparse

from scanner import Scanner


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-H", "--hosts", dest="hosts", type=str,
            nargs="+", default=["127.0.0.1"],
            help=("List of target hosts.\n"
                  "Example: 192.168.0-4.0/24 192.168.15-28.0/24"))
        parser.add_argument("-P", "--ports", dest="ports", type=str,
            nargs="+", default=[19],
            help=("List of target ports.\n"
                  "Example: 15 19 53-69"))
        parser.add_argument("-p", "--proxy", dest="proxies", type=str,
            nargs="+", default=None,
            help=("List of SOCKS5 proxies which will be taken at random.\n"
                  "Example: 98.98.98.98:1080 99.99.99.99:1080"))
        parser.add_argument("-t", "--timeout", dest="timeout",
            type=int, default=1,
            help="How long to wait for reply at UDP request from target host")
        parser.add_argument("-r", "--recheck", dest="recheck", type=int,
            default=0, help="Number of recheck for every port")
        parser.add_argument("-D", "--decoys", dest="decoys", type=str,
            nargs="+", default=None,
            help=("List of decoys to use.\n"
                  "Example: 91.91.91.91 19.19.19.19"))
        parser.add_argument("-i", "--src-int-address", dest="src_int_address",
            type=str, required=True,
            help=("Address of local source interface to listen on.\n"
                  "Example: 192.168.0.15"))
        args = parser.parse_args()

        s = Scanner(args.proxies, args.decoys, args.hosts, args.ports,
            args.timeout, args.recheck, args.src_int_address)
        result = s.scan()
        sorted_ips = sorted(result.keys())
        print("\n")
        for ip in sorted_ips:
            if ip not in ["current_ip", "current_port"]:
                sorted_ports = sorted(result[ip].keys())
                for port in sorted_ports:
                    print("{}:{}\t{}".format(ip, port, result[ip][port]))

    except KeyboardInterrupt:
        print('\nThe process was interrupted by the user')
        raise SystemExit


if __name__ == "__main__":
    main()