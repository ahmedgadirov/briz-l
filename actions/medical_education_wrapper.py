print("Importing medical education actions...")
try:
    from medical_education.actions.action_educate import ActionEducate, ActionSearchEducation, ActionListConditions
    print("Successfully imported medical education actions: ActionEducate, ActionSearchEducation, ActionListConditions")
except Exception as e:
    print(f"Failed to import medical education actions: {e}")
    import traceback
    traceback.print_exc()
