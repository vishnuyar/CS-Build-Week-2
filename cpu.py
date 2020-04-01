"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    

    def __init__(self):
        """Construct a new CPU."""
        #Operation Codes
        self.HLT = 0b00000001
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.MUL = 0b10100010
        self.PUSH = 0b01000101
        self.POP = 0b01000110
        self.CALL = 0b01010000
        self.RET = 0b00010001
        self.ADD = 0b10100000
        self.ST = 0b10000100
        self.CMP = 0b10100111
        self.JEQ = 0b01010101
        self.PRA = 0b01001000
        self.LD = 0b10000011
        self.INC = 0b01100101
        self.DEC = 0b01100110
        self.JMP = 0b01010100
        self.JNE = 0b01010110
        self.AND = 0b10101000
        self.OR = 0b10101010
        self.XOR = 0b10101011
        self.NOT = 0b01101001
        self.SHL = 0b10101100
        self.SHR = 0b10101101
        self.MOD = 0b10100100
        self.message = []
        #StackPointer Starting Address
        self.stackpointer = 0b11110011
        #Initialise RAM
        self.ram = [None]*255
        #Initialise 8 Registers
        self.reg = [0]*8
        self.reg[7] = 0b11110100
        #Initialise Internal Registers
        self.pc = 0
        self.IR = None
        self.MAR = None
        self.MDR = None
        self.FL = 0b00000000

    def load(self,program):
        """Load a program into memory."""
        address = 0
        #Loading in the program in to the RAM
        program = program.replace('You see a faint pattern in the water...','')     
        program = program.replace('\\n',' ').split('\n')
        #print(type(program))
        #print(f'lenght:{len(program)}')
        for line in program:
            if len(line) > 0:
                #print(line)
                instruction = int(line,2)
                #print(f'int:{instruction}')
                self.ram[address] = instruction
                address += 1

            
            


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "MOD":
            if self.reg[reg_b] != 0:
                self.reg[reg_a] %= self.reg[reg_b]
            else:
                raise Exception("Zero value not suppoter for Modulus")
        elif op == "INC":
            self.reg[reg_a] += 1
        elif op == "DEC":
            self.reg[reg_a] -= 1
        elif op == "AND":
            self.reg[reg_a] &= self.reg[reg_b]
        elif op == "OR":
            self.reg[reg_a] |= self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] ^= self.reg[reg_b]
        elif op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == "SHL":
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        elif op == "SHR":
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] > self.reg[reg_b]:
                self.FL = 0b00000010
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.FL = 0b00000100
            else:
                self.FL = 0b00000001
        else:
            raise Exception("Unsupported ALU operation")
    
    def ram_read(self,address):
        return self.ram[address]

    def ram_write(self,address,value):
        self.ram[address] = value
        

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        
        while True:
            instruction = self.ram[self.pc]
            #print(f'instruction:{instruction}')
            if instruction == self.HLT:
                return
            elif instruction == self.PRN:
                self.pc += 1
                reg_address = self.ram[self.pc]
                reg_value = self.reg[reg_address]
                self.message.append(reg_value)
                
            elif instruction == self.LDI:
                self.pc +=1
                reg_address = self.ram[self.pc]
                self.pc +=1
                value = self.ram[self.pc]
                self.reg[reg_address] = value
            elif instruction == self.INC:
                self.pc +=1
                reg_a = self.ram[self.pc]
                self.alu('INC',reg_a,1)
            elif instruction == self.DEC:
                self.pc +=1
                reg_a = self.ram[self.pc]
                self.alu('DEC',reg_a, -1)
            elif instruction == self.MUL:
                self.pc +=1
                reg_a = self.ram[self.pc]
                self.pc +=1
                reg_b = self.ram[self.pc] 
                self.alu('MUL',reg_a,reg_b)
            elif instruction == self.ADD:
                self.pc +=1
                reg_a = self.ram[self.pc]
                self.pc +=1
                reg_b = self.ram[self.pc] 
                self.alu('ADD',reg_a,reg_b)
            elif instruction == self.CMP:
                self.pc +=1
                reg_a = self.ram[self.pc]
                self.pc +=1
                reg_b = self.ram[self.pc] 
                self.alu('CMP',reg_a,reg_b)
            elif instruction == self.AND:
                self.pc +=1
                reg_a = self.ram[self.pc]
                self.pc +=1
                reg_b = self.ram[self.pc] 
                self.alu('AND',reg_a,reg_b)
            elif instruction == self.OR:
                self.pc +=1
                reg_a = self.ram[self.pc]
                self.pc +=1
                reg_b = self.ram[self.pc] 
                self.alu('OR',reg_a,reg_b)
            elif instruction == self.NOT:
                self.pc +=1
                reg_a = self.ram[self.pc]
                self.pc +=1
                reg_b = self.ram[self.pc] 
                self.alu('NOT',reg_a,reg_b)
            elif instruction == self.XOR:
                self.pc +=1
                reg_a = self.ram[self.pc]
                self.pc +=1
                reg_b = self.ram[self.pc]
                self.alu('XOR',reg_a,reg_b)
            elif instruction == self.SHL:
                self.pc +=1
                reg_a = self.ram[self.pc]
                self.pc +=1
                reg_b = self.ram[self.pc] 
                self.alu('SHL',reg_a,reg_b)
            elif instruction == self.SHR:
                self.pc +=1
                reg_a = self.ram[self.pc]
                self.pc +=1
                reg_b = self.ram[self.pc] 
                self.alu('SHR',reg_a,reg_b)
            elif instruction == self.MOD:
                self.pc +=1
                reg_a = self.ram[self.pc]
                self.pc +=1
                reg_b = self.ram[self.pc] 
                self.alu('MOD',reg_a,reg_b)
            elif instruction == self.PUSH:
                self.pc +=1
                reg_address = self.ram[self.pc]
                self.ram[self.stackpointer] = self.reg[reg_address]
                self.stackpointer -=1
            elif instruction == self.POP:
                self.pc +=1
                reg_address = self.ram[self.pc]
                self.stackpointer +=1
                self.reg[reg_address] = self.ram[self.stackpointer]
            elif instruction == self.CALL:
                self.pc +=1
                register_value = self.reg[self.ram[self.pc]]
                self.pc +=1
                self.ram[self.stackpointer] = self.pc
                self.stackpointer -=1
                self.pc = register_value
                #reduce pc value by 1 to counter the effect of pc incrementer
                self.pc -=1
            elif instruction == self.RET:
                self.stackpointer +=1
                stack_value = self.ram[self.stackpointer]
                self.pc = stack_value
                #reduce pc value by 1 to counter the effect of pc incrementer
                self.pc -=1
            elif instruction == self.JMP:
                self.pc +=1
                reg_a = self.ram[self.pc]
                mem_address = self.reg[reg_a]
                self.pc = mem_address
                #reduce pc value by 1 to counter the effect of pc incrementer
                self.pc -=1
            elif instruction == self.ST:
                self.pc +=1
                reg_a = self.ram[self.pc]
                self.pc +=1
                reg_b = self.ram[self.pc]
                mem_address = self.reg[reg_a]
                reg_value = self.reg[reg_b]
                self.ram[mem_address] = reg_value
            elif instruction == self.JEQ:
                self.pc += 1
                if self.FL == 0b00000001:
                    reg_a = self.ram[self.pc]
                    mem_address = self.reg[reg_a]
                    self.pc = mem_address
                    #reduce pc value by 1 to counter the effect of pc incrementer
                    self.pc -=1
            elif instruction == self.JNE:
                self.pc += 1
                if (self.FL & 1) == 0:
                    reg_a = self.ram[self.pc]
                    mem_address = self.reg[reg_a]
                    self.pc = mem_address
                    #reduce pc value by 1 to counter the effect of pc incrementer
                    self.pc -=1
            elif instruction == self.PRA:
                self.pc += 1
                reg_a = self.ram[self.pc]
                reg_value = self.reg[reg_a]
                self.message.append(chr(reg_value)) 
            elif instruction == self.LD:
                self.pc +=1
                reg_a = self.ram[self.pc]
                self.pc +=1
                reg_b = self.ram[self.pc]
                mem_address = self.reg[reg_b]
                reg_value = self.ram[mem_address]
                self.reg[reg_a] = reg_value
            else:
                print("instruction not available")
                print(bin(instruction))
                
                
            self.pc +=1
        