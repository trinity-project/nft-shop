import bcrypt, datetime, sys

if __name__ == "__main__":
    usrid = '123456' # user id
    # t = datetime.datetime.now().strftime('%Y%m%d')
    secret = "!QWWpigxo1970q~"
    salt = bcrypt.gensalt(rounds=10)
    hashed = bcrypt.hashpw(secret, salt)
    print(salt)
    print(hashed)
    # verify_hashed = "$2y$10$2BvqE1jHoJg5jpJRNYOhk.kV3t4CGn/1yA1plSvuK.GK8v/Jkmjj."
    # new_hashed = bcrypt.hashpw("killqrf123", hashed)
    print bcrypt.checkpw(secret, hashed)
    # print(new_hashed)
    # print(hashed == new_hashed)
    # print secret
    # print hashed
    # print len(hashed)
    # print '%d.%d.%d' % (sys.version_info[:3])