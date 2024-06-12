import random
from datetime import datetime

# The AnimalRecord class has all the information about an animal that has been into the vet clinic. 
class AnimalRecord:
    #Creating the animal record.
    def __init__(self, animal_id, animal_type, name, sex, birthday, breed, contact_person, phone_number):
        self.id = animal_id
        self.animal_type = animal_type
        self.name = name
        self.sex = sex
        self.birthday = birthday
        self.breed = breed
        #contact person is the legal owner of the animal
        self.contact_person = contact_person
        self.phone_number = phone_number
        self.notes = ""
        self.appointments = []

    #Adding an appointment to the animal record.
    def add_appointment(self, appointment):
        self.appointments.append(appointment)

    #Adding notes to the animal record.
    def add_notes(self, note):
        self.notes += str(datetime.now()) + ": " + note + "\n"

    #Getting the summary of the animal record.???????
    def get_summary(self):
        summary = "ID   Date    Services    Cost    Status  Payment Status  Amount Left to Pay\n"
        for appointment in self.appointments:
            services_desc = ""
            for service in appointment.services:
                if services_desc:
                    services_desc += ", "
                services_desc += service['name']
            remaining_amount = appointment.cost - appointment.amount_paid
            summary += f"{appointment.id}    {appointment.date}    {services_desc}    ${appointment.cost}    {appointment.status}    {appointment.payment_status}    ${remaining_amount}\n"
        return summary

#The Appointment class has all the information about the animal appointment
class Appointment:
    def __init__(self, appointment_id, date, services, cost):
        self.id = appointment_id
        self.date = date
        #Appointments consist of services.
        self.services = services
        self.cost = cost
        #The status of the appointment can be open or closed. If the appointment is closed, it means that the animal has been treated.If there are too many open appointmnet, the clinic will not be able to accept new appointments.
        self.status = "open"
        self.payment_status = "not paid"
        #The amount paid by the owner of the animal.
        self.amount_paid = 0.0 

#The VetClinic class has all the information about the vet clinic. It has the records of the animals that have been in the clinic, the services that the clinic provides, the capacity of the clinic and the open slots that the clinic has.
class VetClinic:
    def __init__(self):
        self.records = {}
        self.services = self.load_services()
        #The number of open slots that the vet clinic has. Meaning that if they have 20 open appintments, they can't accept new appointments.
        self.capacity = 20

#This method reads the services from the services.txt file and returns them as a dictionary.
    def load_services(self):
        services = {}
        with open("services.txt", "r") as file:
            for line in file:
                key, name, price = line.strip().split(',')
                services[key] = {"name": name, "price": int(price)}
        return services

#This method generates a unique ID for the animal record and the appointment.
    def generate_unique_id(self):
        unique_id = random.randint(1000, 9999)
        id_exists = False

        for record in self.records.values():
            if unique_id == record.id:
                id_exists = True
                break
            for appointment in record.appointments:
                if unique_id == appointment.id:
                    id_exists = True
                    break

        while id_exists:
            unique_id = random.randint(1000, 9999)
            id_exists = False
            for record in self.records.values():
                if unique_id == record.id:
                    id_exists = True
                    break
                for appointment in record.appointments:
                    if unique_id == appointment.id:
                        id_exists = True
                        break

        return unique_id

#This method creates an animal record.
    def create_animal_record(self):
        animal_type = input("Enter animal type: ")
        name = input("Enter animal name: ")
    #User can only enter "f" or "m" for the sex value.This part of the code checks if the user entered a valid value.
        while True:
            sex = input("Enter animal sex (f for female, m for male): ").lower()
            if sex in ['f', 'm']:
                break
            else:
                print("Invalid option. Please enter 'f' for female or 'm' for male.")

        birthday = input("Enter animal birthday (YYYY-MM-DD): ")
        breed = input("Enter animal breed (if applicable): ")
        contact_person = input("Enter contact person: ")
        phone_number = input("Enter phone number: ")

    #The date should be in the format of YYYY-MM-DD. This part of the code checks if the user entered a valid date.
        try:
            datetime.strptime(birthday, '%Y-%m-%d')
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
            return

        animal_id = self.generate_unique_id()
        record = AnimalRecord(animal_id, animal_type, name, sex, birthday, breed, contact_person, phone_number)
        self.records[animal_id] = record
        print("Animal record created with ID: " + str(animal_id))

    #This method adds an appointment to the animal record.
    def add_appointment(self):
        #During this part of code I check if there are open slots avaliable in the clinic. If there are no open slots, the clinic will not be able to accept new appointments.
        if self.get_open_slots() <= 0:
            print("No open slots available for appointments.")
            return

        record_id = int(input("Enter animal ID: "))
        if record_id in self.records:
            date = input("Enter appointment date (YYYY-MM-DD): ")
             #The date should be in the format of YYYY-MM-DD. This part of the code checks if the user entered a valid date.
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
                return

            selected_services = []
            total_cost = 0
            while True:
                print("\nServices:")
                for key, service in self.services.items():
                    print(str(key) + ". " + service['name'] + " - " + str(service['price']) + " GEL")
                service_choice = input("Choose a service by number (or 'done' to finish): ")
                if service_choice.lower() == 'done':
                    break
                if service_choice in self.services:
                    selected_services.append(self.services[service_choice])
                    total_cost += self.services[service_choice]['price']
                else:
                    print("Invalid choice, please try again.")
            appointment_id = self.generate_unique_id()
            appointment = Appointment(appointment_id, date, selected_services, total_cost)
            self.records[record_id].add_appointment(appointment)
            print("Appointment added.")
        else:
            print("Record not found.")

    #This method saves the the medical history of the animal (animal record and it's appintments) as a txt file.
    def get_medical_history(self):
        record_id = int(input("Enter animal ID: "))
        if record_id in self.records:
            summary = self.records[record_id].get_summary()
            file_name = f"medical_history_{record_id}.txt"
            with open(file_name, 'w') as file:
                file.write(summary)
            print("Medical history saved to " + file_name)
        else:
            print("Record not found.")

    #This method adds notes to the animal record.
    def add_notes(self):
        record_id = int(input("Enter animal ID: "))
        if record_id in self.records:
            note = input("Enter note: ")
            self.records[record_id].add_notes(note)
            print("Note added.")
        else:
            print("Record not found.")

    #This method allows the user to pay for the services that the animal received.In order to pay you should choose an animal record (by ID) and then choose the appointment (by ID). Payments can be made in parts or fully. If the payment is fully paid, the payment status will be "fully paid". If the payment is made in parts, the payment status will be "partly paid".
    def pay_for_services(self):
        record_id = int(input("Enter animal ID: "))
        if record_id in self.records:
            print("Appointments:")
            for app in self.records[record_id].appointments:
                #User can only pay for the open appointments.
                if app.status == "open":
                    remaining_amount = app.cost - app.amount_paid
                    service_names = ""
                    for service in app.services:
                        if service_names:
                            service_names += ", "
                        service_names += service['name']
                    print("ID: " + str(app.id) + 
                        ", Date: " + str(app.date) + 
                        ", Services: " + service_names + 
                        ", Cost: " + str(app.cost) + 
                        ", Payment Status: " + str(app.payment_status) + 
                        ", Amount Left to Pay: " + str(remaining_amount))
            appointment_id = int(input("Enter the appointment ID to pay for: "))
            for app in self.records[record_id].appointments:
                if app.id == appointment_id:
                    if app.payment_status == "fully paid":
                        print("This appointment is already fully paid.")
                        return
                    amount_due = app.cost - app.amount_paid
                    print("Total cost is $" + str(app.cost) + 
                        ". Amount already paid is $" + str(app.amount_paid) + 
                        ". Amount left to pay is $" + str(amount_due) + ".")
                    #This part of the code checks if the user entered a valid (numeric) amount.
                    try:
                        amount_paid = float(input("Enter payment amount: "))
                    except ValueError:
                        print("Invalid amount. Please enter a numeric value.")
                        return
                    #This part of the code checks if the amount paid is more than the amount due,if so - the user will get an error message.
                    if amount_paid > amount_due:
                        print(f"Error: Payment amount exceeds the amount due. Amount left to pay is ${amount_due}.")
                    else:
                        #This part of the code determines if the appointment is paid fully or partly.
                        app.amount_paid += amount_paid
                        if app.amount_paid >= app.cost:
                            app.payment_status = "fully paid"
                            print("Payment successful. Appointment fully paid.")
                        else:
                            app.payment_status = "partly paid"
                            print("Payment successful. $" + str(amount_paid) + " paid, $" + str(app.cost - app.amount_paid) + " remaining.")
                    break
        else:
            print("Record not found.")

    #This function gives the user the ability to close an appointment. 
    def close_appointment(self):
        record_id = int(input("Enter animal ID: "))
        if record_id in self.records:
            print("Appointments:")
            for app in self.records[record_id].appointments:
                service_names = ""
                for service in app.services:
                    if service_names:
                        service_names += ", "
                    service_names += service['name']
                print("ID: " + str(app.id) + 
                    ", Date: " + str(app.date) + 
                    ", Services: " + service_names + 
                    ", Cost: " + str(app.cost) + 
                    ", Status: " + str(app.status) + 
                    ", Payment Status: " + str(app.payment_status))
            appointment_id = int(input("Enter the appointment ID to close: "))
            for app in self.records[record_id].appointments:
                if app.id == appointment_id:
                    app.status = "closed"
                    print("Appointment closed.")
                    break
        else:
            print("Record not found.")

    #This function calculates the number of open slots that the clinic has.
    def get_open_slots(self):
        total_appointments = 0
        total_appointments = 0
        for record in self.records.values():
            for app in record.appointments:
                if app.status == "open":
                    total_appointments += 1
        return self.capacity - total_appointments

#This function displays the menu and using the input from the user, calls the appropriate method.
def main():
    clinic = VetClinic()
    while True:
        print("\nMenu:")
        print("1. Create an animal record")
        print("2. Add appointment")
        print("3. Get medical history")
        print("4. Pay for an appointment")
        print("5. Add note to an animal record")
        print("6. Close an appointment")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            clinic.create_animal_record()
        elif choice == '2':
            clinic.add_appointment()
        elif choice == '3':
            clinic.get_medical_history()
        elif choice == '4':
            clinic.pay_for_services()
        elif choice == '5':
            clinic.add_notes()
        elif choice == '6':
            clinic.close_appointment()
        elif choice == '7':
            break
        else:
            print("Incorrect menu item, please try again.")

if __name__ == "__main__":
    main()
