# Vet Clinic Console Program

This console program allows the vet clinic staff to manage the medical records of the animals treated at the clinic. It also tracks appointments, open slots, and payments.

## Classes

### 1. `AnimalRecord`
This class contains all the information about an animal's medical history. 

#### Methods
- `add_appointment(appointment)`: Adds an appointment to the specific record.
- `add_notes(note)`: Adds a note to the specific record.
- `get_summary()`: Summarizes an appointment.

### 2. `Appointment`
This class contains all the information about an animal's medical appointment.

### 3. `VetClinic`
This class contains all the information about the vet clinic, including records of animals treated, services provided, clinic capacity, and open slots.

#### Methods
- `load_services(filename)`: Reads the service list (with prices) from a text file (services.txt).
- `generate_unique_id()`: Generates a unique ID for records and appointments.
- `create_animal_record(animal_info)`: Creates an animal medical record.
- `add_appointment(animal_id, appointment)`: Creates and adds a medical appointment.
- `get_medical_history(animal_id)`: Creates a text file with the animal's medical history (info about appointments).
- `add_note_to_record(animal_id, note)`: Adds notes to an animal's record.
- `pay_for_services(animal_id, amount)`: Allows customers to pay for the appointment.
- `close_appointment(appointment_id)`: Changes an appointment's status to closed.
- `get_open_slots()`: Returns the number of open slots the clinic has.

