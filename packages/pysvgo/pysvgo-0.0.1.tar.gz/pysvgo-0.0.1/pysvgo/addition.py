# addition.py
# Each new plugin class has to be named Plugin 
class Plugin: 
    # This is the feature offer by this plugin.
    # it prints the result of adding 2 numbers  
    def process(self, num1, num2):
        print("This is my addition plugin")
        print(num1 + num2) 