import psycopg
connection = psycopg.connect(host="localhost", dbname="Portal_De_Operações_py", user="postgres", password="DollarBills18!", port=5432)

def saving_history(connection, initial_temperature, initial_value, final_temperature, result):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO conversions_history (initial_temperature, initial_value, final_temperature, result_value)
            VALUES (%s, %s, %s, %s)
            """, (initial_temperature, initial_value, final_temperature, result))
    connection.commit()
 
def show_history(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
SELECT
id,
initial_temperature,
initial_value,
final_temperature,
result_value,
conversion_date
FROM conversions_history
ORDER BY id DESC
""")
        history = cursor.fetchall()
    print("CONVERSION HISTORY")
    if not history:
        print("No conversions found.")
        return
    for conversion in history:
        print(f"ID: {conversion[0]} | {conversion[2]} | {conversion[1]} | {conversion[4]} | {conversion[3]} | {conversion[5]}")

def celsius_converter(initial_temperature, temperature_value):
    if initial_temperature in ["FAHRENHEIT", "°F", "F"]:
        celsius_result = (temperature_value - 32) * 5 / 9
        return celsius_result
    elif initial_temperature in ["KELVIN", "°K", "K"]:
        celsius_result = temperature_value - 273.15
        return celsius_result
    elif initial_temperature in ["RANKINE", "°R", "R"]:
        celsius_result = (temperature_value - 491.67) * 5 / 9
        return celsius_result
    elif initial_temperature in ["RÉAUMUR", "°RE", "RE"]:
        celsius_result = temperature_value * 5 / 4
        return celsius_result
    elif initial_temperature in ["CELSIUS", "°C", "C"]:
        celsius_result = temperature_value
        return celsius_result
    else:
        return None

def fahrenheit_converter(initial_temperature, temperature_value):
    if initial_temperature in ["CELSIUS", "°C", "C"]:
        fahrenheit_result = (temperature_value * 9 / 5) + 32
        return fahrenheit_result
    elif initial_temperature in ["KELVIN", "°K", "K"]:
        fahrenheit_result = (temperature_value - 273.15) * 9 / 5 + 32
        return fahrenheit_result
    elif initial_temperature in ["RANKINE", "°R", "R"]:
        fahrenheit_result = temperature_value - 459.67
        return fahrenheit_result
    elif initial_temperature in ["RÉAUMUR", "°RE", "RE"]:
        fahrenheit_result = temperature_value * 9 / 4 + 32
        return fahrenheit_result
    elif initial_temperature in ["FAHRENHEIT", "°F", "F"]:
        fahrenheit_result = temperature_value
        return fahrenheit_result
    else:
        return None

def kelvin_converter(initial_temperature, temperature_value):
    if initial_temperature in ["CELSIUS", "°C", "C"]:
        kelvin_result = temperature_value + 273.15
        return kelvin_result
    elif initial_temperature in ["FAHRENHEIT", "°F", "F"]:
        kelvin_result = (temperature_value - 32) * 5 / 9 + 273.15
        return kelvin_result
    elif initial_temperature in ["RANKINE", "°R", "R"]:
        kelvin_result = temperature_value * 5 / 9
        return kelvin_result
    elif initial_temperature in ["RÉAUMUR", "°RE", "RE"]:
        kelvin_result = temperature_value * 5 / 4 + 273.15
        return kelvin_result
    elif initial_temperature in ["KELVIN", "°K", "K"]:
        kelvin_result = temperature_value
        return kelvin_result
    else:
        return None

def rankine_converter(initial_temperature, temperature_value):
    if initial_temperature in ["CELSIUS", "°C", "C"]:
        rankine_result = (temperature_value + 273.15) * 9 / 5
        return rankine_result
    elif initial_temperature in ["FAHRENHEIT", "°F", "F"]:
        rankine_result = temperature_value + 459.67
        return rankine_result
    elif initial_temperature in ["KELVIN", "°K", "K"]:
        rankine_result = temperature_value * 9 / 5
        return rankine_result
    elif initial_temperature in ["RÉAUMUR", "°RE", "RE"]:
        rankine_result = (temperature_value * 5 / 4 + 273.15) * 9 / 5
        return rankine_result
    elif initial_temperature in ["RANKINE", "°R", "R"]:
        rankine_result = temperature_value
        return rankine_result
    else:
        return None

def reaumur_converter(initial_temperature, temperature_value):
    if initial_temperature in ["CELSIUS", "°C", "C"]:
        reaumur_result = temperature_value * 4 / 5
        return reaumur_result
    elif initial_temperature in ["FAHRENHEIT", "°F", "F"]:
        reaumur_result = (temperature_value - 32) * 4 / 9
        return reaumur_result
    elif initial_temperature in ["KELVIN", "°K", "K"]:
        reaumur_result = (temperature_value - 273.15) * 4 / 5
        return reaumur_result
    elif initial_temperature in ["RANKINE", "°R", "R"]:
        reaumur_result = (temperature_value - 491.67) * 4 / 9
        return reaumur_result
    elif initial_temperature in ["RÉAUMUR", "°RE", "RE"]:
        reaumur_result = temperature_value
        return reaumur_result
    else:
        return None

def conversions_execution(connection):
    while True:
        try:
            initial_temperature = input("Choose the temperature to be converted: ").strip().upper()
            valid_scales = ["CELSIUS", "°C", "C", "FAHRENHEIT", "°F", "F", "KELVIN", "°K", "K", "RANKINE", "°R", "R", "RÉAUMUR", "°RE", "RE"]
            if initial_temperature not in valid_scales:
                raise ValueError("Invalid initial temperature scale.")
            final_temperature = input("Choose the temperature for conversion's result: ").strip().upper()
            if final_temperature not in valid_scales:
                raise ValueError("Invalid final temperature scale.")
            temperature_value = float(
                input("Type the value of the temperature to be converted: "))
            if final_temperature in ["CELSIUS", "°C", "C"]:
                result = celsius_converter(initial_temperature, temperature_value)
                result_unit = "°C"
            elif final_temperature in ["FAHRENHEIT", "°F", "F"]:
                result = fahrenheit_converter(initial_temperature, temperature_value)
                result_unit = "°F"
            elif final_temperature in ["KELVIN", "°K", "K"]:
                result = kelvin_converter(initial_temperature, temperature_value)
                result_unit = "K"
            elif final_temperature in ["RANKINE", "°R", "R"]:
                result = rankine_converter(initial_temperature, temperature_value)
                result_unit = "°R"
            elif final_temperature in ["RÉAUMUR", "°RE", "RE"]:
                result = reaumur_converter(initial_temperature, temperature_value)
                result_unit = "°Ré"
            print("")
            print("The conversion's result is {result:.2f} {result_unit}.")
            saving_history(connection, initial_temperature, temperature_value, final_temperature, result)
            print("")
            print("Conversion saved to history.")
            print("")
            while True:
                again = input("Do you want to make another conversion? (Yes/No): ").strip().upper()
                if again == "YES":
                    print("Starting a new conversion...")
                    break
                elif again == "NO":
                    print("Thank you for using High-up Converter! Have a great day!")
                    exit()
                else:
                    print("Invalid answer. Please type Yes or No.")
        except ValueError as error:
            print(f"Error: {error}")
            print("Please try again.")
        except psycopg.Error as error:
            print(f"Database error: {error}")
            print("Could not save the conversion.")

def interface(connection):
    while True:
        print("Welcome to High-up Converter!")
        print("Choose one of the following options to proceed: ")
        print("1. New conversion")
        print("2. Your conversion history")
        print("3. Exit")
        try:
            users_choice = int(input("Type the number of your choice: "))
        except ValueError:
            print("Invalid option.")
            print("Please type a valid number (1, 2 or 3).")
            continue
        if users_choice == 1:
            conversions_execution(connection)
        elif users_choice == 2:
            show_history(connection)
        elif users_choice == 3:
            print("Session terminated.")
            print("Thank you for using High-up Converter!")
            connection.close()
            break
        else:
            print("Invalid option.")
            print("Please choose 1, 2 or 3.")

interface(connection)