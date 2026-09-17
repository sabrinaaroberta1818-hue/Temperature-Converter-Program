import os, psycopg, time
os.system("cls")
connection = psycopg.connect(host="localhost", dbname="Portal_De_Operações_py", user="postgres", password="DollarBills18!", port=5432)

def saving_history(connection, initial_temperature, initial_value, final_temperature, result):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO conversions_history(initial_temperature, initial_value, final_temperature, result_value)
            VALUES (%s, %s, %s, %s)
            """,
    (initial_temperature, initial_value, final_temperature, result))
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

def scale_adaptation(temperature_scale):
    scale = temperature_scale.strip().upper()
    scales = {"C": "CELSIUS", "°C": "CELSIUS", "CELSIUS": "CELSIUS", "F": "FAHRENHEIT", "°F": "FAHRENHEIT","FAHRENHEIT": "FAHRENHEIT", "K": "KELVIN", "°K": "KELVIN", "KELVIN": "KELVIN", "R": "RANKINE", "°R": "RANKINE", "RANKINE": "RANKINE", "RE": "REAUMUR", "°RE": "REAUMUR", "REAUMUR": "REAUMUR", "RÉAUMUR": "REAUMUR"}
    return scales.get(scale)

def celsius(initial_temperature, temperature_value):
    if initial_temperature == "FAHRENHEIT":
        return (temperature_value - 32) * 5 / 9
    elif initial_temperature == "KELVIN":
        return temperature_value - 273.15
    elif initial_temperature == "RANKINE":
        return (temperature_value - 491.67) * 5 / 9
    elif initial_temperature == "REAUMUR":
        return temperature_value * 5 / 4
    elif initial_temperature == "CELSIUS":
        return temperature_value
    else:
        return None

def convert_temperature(initial_temperature, temperature_value, final_temperature):
    celsius_result = celsius(initial_temperature, temperature_value)
    if celsius_result is None:
        return None
    if final_temperature == "CELSIUS":
        return celsius_result
    elif final_temperature == "FAHRENHEIT":
        return (celsius_result * 9 / 5) + 32
    elif final_temperature == "KELVIN":
        return celsius_result + 273.15
    elif final_temperature == "RANKINE":
        return (celsius_result + 273.15) * 9 / 5
    elif final_temperature == "REAUMUR":
        return celsius_result * 4 / 5
    else:
        return None

def conversions_execution(connection):
    while True:
        try:
            initial_temperature = scale_adaptation(input("Choose the temperature to be converted: "))
            print("")
            if initial_temperature is None:
                raise ValueError("Invalid initial temperature scale.")
            final_temperature = scale_adaptation(
                input("Choose the temperature for conversion's result: "))
            print("")
            if final_temperature is None:
                raise ValueError("Invalid final temperature scale.")
            temperature_value = float(input("Type the value of the temperature to be converted: "))
            print("")
            result = convert_temperature(initial_temperature, temperature_value, final_temperature)
            result_unit = {"CELSIUS": "°C", "FAHRENHEIT": "°F", "KELVIN": "K", "RANKINE": "°R", "REAUMUR": "°Ré"}[final_temperature]
            print(f"The conversion's result is {result:.2f} {result_unit}.")
            saving_history(connection, initial_temperature, temperature_value, final_temperature, result)
            print("")
            print("Conversion saved to history.")
            print("")
            while True:
                again = input("Do you want to make another conversion? (Yes/No): ").strip().upper()
                if again == "YES":
                    print("")
                    print("Starting a new conversion...")
                    time.sleep(1)
                    print("")
                    break
                elif again == "NO":
                    print("")
                    print("Thank you for using High-up Converter! Have a great day!")
                    connection.close()
                    return
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