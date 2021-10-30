SET logfile="C:\Reports\batch.log"
@echo off
@echo Starting Script at %date% %time% >> %logfile%
"C:\Users\fensk\AppData\Local\Programs\Python\Python39\python.exe" "C:\Users\fensk\Documents\GitHub\LPOS_WooCommerce_Inventory_Sync\Update_Stock.py"
@echo finished at %date% %time% >> %logfile%