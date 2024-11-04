import hashlib
import time
from tabulate import tabulate

# Messages of varying lengths
short_message = "Hi"
medium_message = (
    "Security Threats\n"
    "Computer systems face a number of security threats. One of the basic threats is data loss, "
    "which means that parts of a database can no longer be retrieved. This could be the result of "
    "physical damage to the storage medium (like fire or water damage), human error or hardware "
    "failures. Another security threat is unauthorized access. Many computer systems contain sensitive "
    "information, and it could be very harmful if it were to fall in the wrong hands. Imagine someone "
    "getting a hold of your social security number, date of birth, address and bank information. "
    "Getting unauthorized access to computer systems is known as hacking. Computer hackers have "
    "developed sophisticated methods to obtain data from databases, which they may use for personal gain "
    "or to harm others. A third category of security threats consists of viruses and other harmful "
    "programs. A computer virus is a computer program that can cause damage to a computer's software, "
    "hardware or data. It is referred to as a virus because it has the capability to replicate itself and "
    "hide inside other computer files."
)

long_message = (
    "Instructor: Paul Zandbergen\n"
    "Paul has a PhD from the University of British Columbia and has taught Geographic Information Systems, "
    "statistics and computer programming for 15 years. Computer systems face a number of security threats. "
    "Learn about different approaches to system security, including firewalls, data encryption, passwords "
    "and biometrics.\n"
    "Security Threats\n"
    "Computer systems face a number of security threats. One of the basic threats is data loss, which means "
    "that parts of a database can no longer be retrieved. This could be the result of physical damage to "
    "the storage medium (like fire or water damage), human error or hardware failures.\n"
    "Another security threat is unauthorized access. Many computer systems contain sensitive information, "
    "and it could be very harmful if it were to fall in the wrong hands. Imagine someone getting a hold "
    "of your social security number, date of birth, address and bank information. Getting unauthorized "
    "access to computer systems is known as hacking. Computer hackers have developed sophisticated methods "
    "to obtain data from databases, which they may use for personal gain or to harm others.\n"
    "A third category of security threats consists of viruses and other harmful programs. A computer virus "
    "is a computer program that can cause damage to a computer's software, hardware or data. It is referred "
    "to as a virus because it has the capability to replicate itself and hide inside other computer files.\n"
    "System Security\n"
    "The objective of system security is the protection of information and property from theft, corruption "
    "and other types of damage, while allowing the information and property to remain accessible and productive. "
    "System security includes the development and implementation of security countermeasures. There are a number "
    "of different approaches to computer system security, including the use of a firewall, data encryption, "
    "passwords and biometrics.\n"
    "Firewall\n"
    "One widely used strategy to improve system security is to use a firewall. A firewall consists of software "
    "and hardware set up between an internal computer network and the Internet. A computer network manager sets "
    "up the rules for the firewall to filter out unwanted intrusions. These rules are set up in such a way that "
    "unauthorized access is much more difficult.\n"
    "A system administrator can decide, for example, that only users within the firewall can access particular "
    "files, or that those outside the firewall have limited capabilities to modify the files. You can also set "
    "up a firewall for your own computer, and on many computer systems, this is built into the operating system.\n"
    "Encryption\n"
    "One way to keep files and data safe is to use encryption. This is often used when data is transferred over "
    "the Internet, where it could potentially be seen by others. Encryption is the process of encoding messages "
    "so that it can only be viewed by authorized individuals. An encryption key is used to make the message "
    "unreadable, and a secret decryption key is used to decipher the message.\n"
    "Encryption is widely used in systems like e-commerce and Internet banking, where the databases contain "
    "very sensitive information. If you have made purchases online using a credit card, it is very likely that "
    "you've used encryption to do this.\n"
    "Passwords\n"
    "The most widely used method to prevent unauthorized access is to use passwords. A password is a string of "
    "characters used to authenticate a user to access a system. The password needs to be kept secret and is "
    "only intended for the specific user. In computer systems, each password is associated with a specific "
    "username since many individuals may be accessing the same system.\n"
    "Good passwords are essential to keeping computer systems secure. Unfortunately, many computer users don't "
    "use very secure passwords, such as the name of a family member or important dates - things that would be "
    "relatively easy to guess by a hacker. One of the most widely used passwords - you guessed it - 'password.' "
    "Definitely not a good password to use.\n"
    "So what makes for a strong password?\n"
    "● Longer is better - A long password is much harder to break. The minimum length should be 8 characters, "
    "but many security experts have started recommending 12 characters or more.\n"
    "● Avoid the obvious - A string like '0123456789' is too easy for a hacker, and so is 'LaDyGaGa'. You should "
    "also avoid all words from the dictionary.\n"
    "● Mix it up - Use a combination of upper and lowercase and add special characters to make a password much stronger. "
    "A password like 'hybq4' is not very strong, but 'Hy%Bq&4$' is very strong.\n"
    "Remembering strong passwords can be challenging. One tip from security experts is to come up with a sentence "
    "that is easy to remember and to turn that into a password by using abbreviations and substitutions. For example, "
    "'My favorite hobby is to play tennis' could become something like Mf#Hi$2Pt%.\n"
    "Regular users of computer systems have numerous user accounts. Just consider how many accounts you use on a "
    "regular basis: email, social networking sites, financial institutions, online shopping sites and so on. A "
    "regular user of various computer systems and web sites will have dozens of different accounts, each with a "
    "username and password. To make things a little bit easier on computer users, a number of different approaches "
    "have been developed."
)

# Number of times to run each hash for averaging
REPEAT_COUNT = 1000


# Helper function to calculate average hash time in nanoseconds
def calculate_avg_hash_time(message, hash_function):
    total_time = 0
    for _ in range(REPEAT_COUNT):
        start_time = time.perf_counter()
        if hash_function == "MD5":
            hashlib.md5(message.encode()).hexdigest()
        elif hash_function == "SHA512":
            hashlib.sha512(message.encode()).hexdigest()
        end_time = time.perf_counter()
        total_time += end_time - start_time
    avg_time = (total_time / REPEAT_COUNT) * 1e9  # Convert to nanoseconds
    return avg_time


# Collect data
data = []
for msg, label in [
    (short_message, "Short ('Hi')"),
    (medium_message, "Medium"),
    (long_message, "Long"),
]:
    md5_avg_time = calculate_avg_hash_time(msg, "MD5")
    sha512_avg_time = calculate_avg_hash_time(msg, "SHA512")

    data.append(
        [
            label,
            len(msg),
            "128 bits",
            "512 bits",  # Output sizes for MD5 and SHA-512
            f"{md5_avg_time:.2f} ns",
            f"{sha512_avg_time:.2f} ns",
        ]
    )

# Display the table
headers = [
    "Message",
    "Input Size (chars)",
    "MD5 Output Size",
    "SHA-512 Output Size",
    "MD5 Avg Time (ns)",
    "SHA-512 Avg Time (ns)",
]
print(tabulate(data, headers=headers, tablefmt="grid"))
