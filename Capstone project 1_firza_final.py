#load data dari file json
#data base dalam format dictionary dalam list yang berisi:
# [{origin: string, asal daerah kopi
#  proses: string, proses paska panen
#  harga: integer, harga dalam satuan rupiah / gram, untuk mempermudah pencatatan stok
#  stok: integer, stok yang tersedia, dalam satuan gram
#  roaster:string, nama roastery}]
import json
with open("C:\\Users\\Lenovo\\Desktop\\Datascience PWDK\\Py files\\Capstone 1\\capstone_coffee_dataset.json","r") as file:
    data_biji_kopi = json.load(file)
# data_biji_kopi = [] #disiapkan untuk melakukan testing "no data notification"

#fitur saving dibuat function agar bisa digunakan berkali, memastikan setiap perubahan yand dilakukan akan tersimpan di database
def save_data(data):
    with open("C:\\Users\\Lenovo\\Desktop\\Datascience PWDK\\Py files\\Capstone 1\\capstone_coffee_dataset.json", "w") as file:
        json.dump(data, file, indent=4)


def main_menu ():
    while True:
        print('''Pilih menu dibawah ini:
                1. Daftar item
                2. Menambah data
                3. update data
                4. menghapus data
                5. transaksi
                6. keluar aplikasi  ''')
        try:
            input_awal = int(input('silahkan pilih opsi 1/2/3/4/5/6 '))
            if input_awal > 6 or input_awal < 1:
                print('diluar opsi!')
                continue
            if input_awal == 1:     #fitur read : menunjukan data dan filter data                                                 
                daftar_data(data_biji_kopi)

            elif input_awal == 2:   #fitur create : menambahkan data baru ke database                                                    
                menu_tambah_data(data_biji_kopi)    

            elif input_awal == 3:   #fitur update : memperbaharui data pada database
                menu_update_data(data_biji_kopi)

            elif input_awal == 4:   #fitur delete : menghapus data yang ada pada database
                menu_hapus_data(data_biji_kopi)

            elif input_awal == 5:   #fitur tambahan : fitur transaksi yang bisa membaca data dan menambah data baru pada list sementara, dan akan mengupdate database sesuai dengan jumlah pembelian
                transaksi(data_biji_kopi)
            
            elif input_awal == 6: 
                quit()
                
        except ValueError:
            print('silahkan masukan angka sesuai opsi!')

#pada code ini, fitur show item memiliki 2 kegunaan
def show_item (data):
    #1. untuk melakukan pengecekan ketersediaan data 
    panjang_data = len(data)
    if panjang_data == 0: 
        print('data tidak ditemukan, silahkan import library atau menambah data')
        return False
    
    #2. untuk memperlihatkan tabel item secara berulang
    elif panjang_data > 0: 
        print("-" * 74)
        print(f'no.index| origin\t| proses\t| harga\t     | stock   | roaster |')
        print("-" * 74)
        for item in range(panjang_data):
            print(f'{str(item).ljust(8)}| {(data[item]['origin']).ljust(14)}| {(data[item]['proses']).ljust(14)}|{str(data[item]['harga']).rjust(5)} (/gr) | {str(data[item]['stock']).ljust(8)}| {(data[item]['roaster']).ljust(8)}| ')
        return True
    
#fitur ini digunakan untuk memperlihatkan tabel yang dirasa tidak memerlukan kolom index
def show_item_no_index(data):
    print("-" * 59)
    print(f' origin\t       | proses    | harga     | stock   | roaster |')
    print("-" * 59)
    panjang_list_temp = len(data)
    for i in range(panjang_list_temp): #menampilkan baris sesuai dengan jumlah data
        print(f' {(data[i]['origin']).ljust(14)}| {(data[i]['proses']).ljust(10)}|{str(data[i]['harga']).rjust(5)}(/gr) | {str(data[i]['stock']).ljust(8)}| {(data[i]['roaster']).ljust(8)}| ')

def daftar_data(data): 
    while True:
        print('''pilih opsi:
          1. melihat semua data
          2. filter data
          3. kembali ke halaman utama''')
#failsafe method yang akan sering digunakan pada kode ini adalah try-except pada input integer dan .lower untuk input string
        try:
            input_daftar_data = int(input('masukan opsi [1/2/3] ' ))
            if input_daftar_data < 0 or input_daftar_data > 3: #memastikan bahwa user hanya bisa memasukan angka sesuai jumlah pilihan
                print('diluar opsi!')
                continue

            #menunjukan semua data yang tersimpan
            elif input_daftar_data == 1: 
                show_item(data_biji_kopi) 

            #berpindah ke menu filter data             
            elif input_daftar_data == 2: 
                filter_data(data_biji_kopi)

            #kembali ke menu sebelumnya (main menu) 
            elif input_daftar_data == 3: 
                return
        except ValueError:
            print('input harus berupa angka!')

#function ini akan memilah data berdasarkan opsi yang dipilih
def filter_data(data):
    #mengecek ketersediaan data
    if not show_item(data):
        return 
    
    while True:
        print('''data dapat difilter berdasarkan:
                1. origin
                2. roaster
                3. proses
                4. rentang harga
                5. rentang stock
                00. kembali ke menu sebelumnya''')
        
        #list sementara untuk menyimpan data yang lolos filtrasi
        list_filter = [] 
        jumlah_data = len(data)
        
        #disini tidak digunakan try-except agar user dapat memasukan selain angka
        input_filter = input('filter berdasarkan apa? ').lower() 
    
        #filter berdasarakan origin
        if input_filter == 'origin' or input_filter == '1':       
            input_filter_origin = input('masukan nama origin ').lower() 
            for i in range(jumlah_data):
        # Menggunakan in agar sedikit memberikan keleluasaan bagi user, 
        # sama seperti pada filtrasi proses dan roaster      
                if input_filter_origin in data[i]['origin']: 
                    list_filter.append(data[i])

        #filter berdasarakan roaster
        elif input_filter == 'roaster' or input_filter == '2':
            input_filter_roaster = input ('masukan nama roaster ').lower()
            for i in range(jumlah_data):
                if input_filter_roaster in data[i]['roaster']:
                    list_filter.append(data[i])
                

        #filter berdasarakan proses
        elif input_filter == 'proses' or input_filter == '3': 
            input_filter_proses = input ('masukan nama proses ').lower()
            for i in range(jumlah_data):
                if input_filter_proses in data[i]['proses']:
                    list_filter.append(data[i])   

        #filter berdasarakan rentang harga
        elif input_filter == 'harga' or input_filter == 'rentang harga' or input_filter == '4':
            try:
                input_harga_maksimal = int(input('masukan harga maksimal per gram  '))
            except ValueError:
                print('input harus berupa angka')
            try:
                input_harga_minimal = int(input('masukan harga minimal per gram  '))
            except ValueError:
                print('input harus berupa angka')
            for i in range(jumlah_data):
        # menggunakan "and" untuk memastikan hasil yang keluar memenuhi kedua kondisi rentang harga min-max
                if data[i]['harga'] <= input_harga_maksimal and data[i]['harga'] >= input_harga_minimal:
                    list_filter.append(data[i])     
        
        #filter berdasarakan stock
        elif input_filter == 'stock' or input_filter == 'stok' or input_filter == 'rentang stock' or input_filter == '5':    
            try:
                input_stock_maksimal = int(input('masukan stok maksimal '))
            except ValueError:
                print('input harus berupa angka')
            try:
                input_stock_minimal = int(input('masukan stok minimal '))
            except ValueError:
                print('input harus berupa angka')
            for i in range(jumlah_data):
                if data[i]['stock'] <= input_stock_maksimal and data[i]['stock'] >= input_stock_minimal:
                    list_filter.append(data[i])

        #kembali ke sub-menu daftar data
        elif input_filter == '00':
            return
        else:
            print('silahkan pilih berdasarkan opsi!')    
            continue
        
        #menampilkan hasil filter
        panjang_list_filter = len(list_filter)
        #jika filter tidak menghasilkan data
        if panjang_list_filter == 0:
            print('data tidak ditemukan!')
            return
        
        #menampilkan data
        elif panjang_list_filter > 0:    
            show_item(list_filter)            
            return


def menu_tambah_data(data):
    while True:
        print('''opsi:
             1. tambah data
             2. kembali ke menu awal''')
        try:
            input_opsi_tambah_data = int(input( 'pilih opsi '))
            if input_opsi_tambah_data == 1:
                tambah_data(data_biji_kopi)
            elif input_opsi_tambah_data == 2:
                return
            else: 
                print('pilih sesuai opsi!')  
                continue
        except ValueError:
            print('input harus angka!') 

#fitur untuk menambah data baru
def tambah_data(data):
    #input awal agar user bisa menentukan berapa banyak data yang ingin ditambahkan
    try:
        n = int(input("Berapa banyak kopi yang ingin ditambah? "))
        if n <= 0 :
                print('input harus lebih dari 0!')
                return
    except ValueError:
        print("Input harus angka!")
        return
    
    #list sementara sebelum data baru diinput disimpan ke database
    list_sementara = []
    for item in range(n):
        dict_kopi_baru = {'origin'         : '',        
                        'proses'           : '',
                        'harga'            : 0,          
                        'stock'            : 0,
                        'roaster'          : ''} 
        input_origin_baru = input('dari mana origin kopi tersebut? ').lower()
        input_proses_baru = input('Apa prosesnya? ').lower()

        # duplikasi data dicek secara iteratif berdasarkan kombinasi origin dan proses
        duplikasi_data = False #secara default tidak terjadi duplikasi data
        for kopi in data:
            if kopi['origin'] == input_origin_baru and kopi['proses'] == input_proses_baru:
                duplikasi_data = True
                break #langsung menghentikan iterasi jika ditemukan duplikasi
        
        if duplikasi_data: #is true
            print('data sudah ada, jika ingin memperbaharui data, pilih opsi [3. update data] pada menu utama')
            continue # menggunakan continue, agar user dapat lanjut memasukan data kopi setelahnya(jika memilih memasukan lebih dari 1 data baru)

        else:
             dict_kopi_baru['proses'] = input_proses_baru
             dict_kopi_baru['origin'] = input_origin_baru
        #at this point the dictionary will look like this
        #dict_kopi_baru = {'origin'          : 'origin baru',        
                        # 'proses'           : 'proses baru',
                        # 'harga'            : 0,          
                        # 'stock'            : 0,
                        # 'roaster'          : ''} 
        
        #input harga
        while True:
            try:
                input_harga_baru = int(input('berapa harganya? '))
                
                if input_harga_baru <= 0:
                    print('harga harus lebih besar dari 0!')
                    continue

                #kondisi ini untuk melakukan konfirmasi harga yang dimasukan dalam satuan rupiah /gram ataupun kelebihan input angka    
                elif input_harga_baru >= 1000:
                    print('pastikan input harga dalam harga per gram!')
                    while True:
                        input_konfirmasi_harga_per_gram = input('apakah harga yang diinput sudah sesuai? (y/n) ').lower()
                        if input_konfirmasi_harga_per_gram == 'y':
                            dict_kopi_baru['harga'] = input_harga_baru #jika konfirmasi y, akan dimasukan kedalam dict_kopi_baru
                            break

                        elif input_konfirmasi_harga_per_gram == 'n':
                            print('silahkan masukan harga baru!')
                            break

                        else:
                            print('input harus y/n')
                            continue

                    if input_konfirmasi_harga_per_gram == 'n':
                        continue
                    else:
                        break #bertujuan untuk melewati kondisi else dibawah agar tidak terjadi double input
                else:
                    dict_kopi_baru['harga'] = input_harga_baru
                    break
                
            except ValueError:
                print('input harus berupa angka!')
                continue
        #At this point the dictionary will look like this
        #dict_kopi_baru = {'origin'          : 'origin baru',        
                        # 'proses'           : 'proses baru',
                        # 'harga'            : 0(harga baru dalam integer),          
                        # 'stock'            : 0,
                        # 'roaster'          : ''}     
        
        #input stok
        while True:
            try:
                input_stock_baru = int(input('berapa gram stoknya? '))
                if input_stock_baru <= 0:
                    print('stock tidak bisa negatif!')
                    continue 
                dict_kopi_baru['stock'] = input_stock_baru
                break
            except ValueError:
                print('input harus berupa angka!')
                continue
        #at this point the dictionary will look like this
        #dict_kopi_baru = {'origin'          : 'origin baru',        
                        # 'proses'           : 'proses baru',
                        # 'harga'            : x(harga baru dalam integer),          
                        # 'stock'            : y(harga baru dalam integer),
                        # 'roaster'          : ''}        

        #input roaster                
        input_roaster_baru = input('dari roaster mana? ').lower()
        dict_kopi_baru['roaster'] = input_roaster_baru
        #at this point the dictionary will look like this
        #dict_kopi_baru = {'origin'          : 'origin baru',        
                        # 'proses'           : 'proses baru',
                        # 'harga'            : x(harga baru dalam integer),          
                        # 'stock'            : y(harga baru dalam integer),
                        # 'roaster'          : 'roaster baru'}
        
        list_sementara.append(dict_kopi_baru)
        #at this point the list will look like this
        #list_sementara = [
        #               {'origin'            : 'origin baru',        
                        # 'proses'           : 'proses baru',
                        # 'harga'            : x(harga baru dalam integer),          
                        # 'stock'            : y(harga baru dalam integer),
                        # 'roaster'          : 'roaster baru'}
                        # ]
        print('item yang akan ditambahkan:')
        show_item_no_index(list_sementara)
        
    if list_sementara:
        while True:
            input_konfirmasi_save = input('lanjut melakukan save data?(y/n)').lower()
            if input_konfirmasi_save == 'y':
                data.extend(list_sementara)
    #menggunakan .extend agar memasukan dapat memasukan data dalam list_sementara ke data_biji_kopi secara berulang(lebih dari 1)
                save_data(data)
                print('kopi berhasil ditambahkan!')
                show_item(data)
                list_sementara.clear() #memastikan data dalam list sementara terhapus setelah selesai menambah data
                break
            elif input_konfirmasi_save == 'n':
                list_sementara.clear() 
                return
            else:
                print('input harus y/n')
                continue     


def menu_update_data(data):
    while True:
        print('''sub menu update data:
             1. update data
             2. kembali ke menu awal''')
        try:
            input_opsi_update_data = int(input( 'pilih opsi '))
            if input_opsi_update_data == 1:
                update_data(data)
            elif input_opsi_update_data == 2:
                return
            else: 
                print('pilih sesuai opsi!')  
                continue
        except ValueError:
            print('input harus angka!')

#fitur untuk memperbaharui data
def update_data(data):
    #mengecek ketersediaan data
    if not show_item(data):
        return 
    
    while True:
        try:
            input_update_user = int(input('pilih index yang akan diganti '))
            if input_update_user < 0 or input_update_user >= len(data):# memastikan input user berada dalam rentang index
                print('input diluar index!')
                continue
        except ValueError:
            print('input harus berupa angka index!')
            continue

        #tabel dibawah menunjukan item/ kopi berdasarkan index yang user pilih
        print(f'\nanda memilih index {input_update_user}')
        print(f'data biji kopi pada index ini adalah:')
        print(f'origin\t      | proses    | harga     | stock   | roaster  |')
        print(f'{(data[input_update_user]['origin']).ljust(14)}| {(data[input_update_user]['proses']).ljust(10)}| {(str(data[input_update_user]['harga'])).ljust(1)}(/gr)  | {str(data[input_update_user]['stock']).ljust(8)}| {(data[input_update_user]['roaster']).ljust(8)} | ')
        
        #melakukan konfirmasi mengenai index yang dipilih user
        while True: 
            input_konfirmasi_data = input('lanjut melakukan update data?(y/n)').lower()
            if input_konfirmasi_data == 'y':
                break
            elif input_konfirmasi_data == 'n':
                return
            else:
                print('input harus y/n')
                continue   

        #penyimpanan sementara menggunakan dictionary, karena dalam proses akan menyimpan key(kolom) dan value(nilai baru)
        dict_kolom_diubah = {}

        #dalam fitur update ini, user akan terus diminta input kolom dan value baru, sampai ia mengetik selesai
        while True:
                input_update_kolom = input("kolom mana yang akan diganti nilainya? ketik 'selesai' jika tidak ada lagi ").lower()
                if input_update_kolom == 'selesai':
                    if not dict_kolom_diubah:
                        print('\ntidak ada perubahan yang dilakukan')
                        return
                    break
                elif input_update_kolom not in data[input_update_user]:
                    print("masukan sesuai nama kolom! atau input 'selesai' jikatidak ada lagi!")
                    continue
                
        
                print(f'item yang dipilih : \norigin = {data[input_update_user]['origin']} \n{input_update_kolom} = {data[input_update_user][input_update_kolom]} ')
                
                #input value baru,sesuai dengan tipe data
                while True:
                #harga dan stok (integer) memiliki treatment yang berbeda dengan origin, proses dan roaster(string)    
                    if input_update_kolom == 'harga' or input_update_kolom == 'stock':
                        try:
                            input_value_baru = int(input('masukan nilai baru '))
                        except ValueError:
                            print('value harus berupa angka')
                            continue
                    else:
                        input_value_baru = input('masukan nilai baru ').lower()
                    dict_kolom_diubah[input_update_kolom] = input_value_baru
                    #di dititik ini: dict_kolom_diubah = {input_updata_kolom:input_value_baru}
                    break
                
        print("\nKonfirmasi perubahan:")
        #.items digunakan untuk meningkatkan kejelasan syntax
        for kolom, nilai_baru in dict_kolom_diubah.items():
            print(f"{kolom} : {data[input_update_user][kolom]} → {nilai_baru}")
        
        #loop konfirmasi update
        while True:
            input_konfirmasi_update = input(f"apakah anda ingin menyimpan perubahan ini? (y/n) ").lower()
            if input_konfirmasi_update == 'y':
                for kolom, nilai_baru in dict_kolom_diubah.items():
                    data[input_update_user][kolom] = nilai_baru
                print("data berhasil diupdate!")
                save_data(data)
                show_item(data)
                dict_kolom_diubah.clear()
                return   
            elif input_konfirmasi_update == 'n':
                dict_kolom_diubah.clear()
                return
            else:
                print('input harus y/n')
                continue    


def menu_hapus_data(data):
    while True:
        print('''sub-menu penghapusan data
                opsi:
                1. hapus data
                2. kembali ke menu awal''')
        try:
            input_opsi_hapus_data = int(input( 'pilih opsi '))
            if input_opsi_hapus_data == 1:
                hapus_data(data)
            elif input_opsi_hapus_data == 2:
                return
            else: 
                print('pilih sesuai opsi!')  
                continue
        except ValueError:
            print('input harus angka!') 

def hapus_data (data): 
    #memeriksa ketersediaan data
    if not show_item(data):
        return 
    #fitur jika memang ingin menghapus lebih dari 1 data 
    try:
        n = int(input("Berapa banyak kopi yang ingin dihapus? "))
        #memastikan bahwa data yang akan dihapus tidak lebih dari jumlah data yang tersedia
        if n <= 0 or n > len(data):
                print('tidak bisa menghapus 0 data atau lebih dari jumlah data')
                return
    except ValueError:
        print("Input harus angka!")
        return
    #list sementara yang berisikan index yang akan dihapus
    index_to_delete = []
    for idx in range(n):
        try:
            input_index_hapus = int(input('Masukan index yang akan dihapus '))
            if input_index_hapus < 0 or input_index_hapus >= len(data):
                print('diluar index')
                continue
            index_to_delete.append(input_index_hapus)
            #pada titik ini, index_to_delete berbentuk ini :
            #contohnya jika user memilih 2 index untuk diubah, index 0 dan index 3
            # index_to_delete = [0,3]
        except ValueError:
            print('input harus angka!')  
            continue

    print('anda akan menghapus:')
    print(f'index| origin\t\t| proses  | harga  | stock  | roaster |')
    for idx in index_to_delete:
        print(f'{str(idx).ljust(5)}| {(data[idx]['origin']).ljust(15)} \t| {(data[idx]['proses']).ljust(7)} |  {str(data[idx]['harga']).ljust(6)}| {str(data[idx]['stock']).ljust(6)} | {(data[idx]['roaster']).ljust(7)} |')    
    #tabel ini akan menunjukan data dari index yang akan dihapus
    # kurang lebih tabel akan jadi seperti ini:
    #print(f'0 | data[0]['origin'] | data[0]['proses'] | data[0][harga]|data[0][stock] | data [0]['roaster']|)
    #print(f'3 | data[3]['origin'] | data[3]['proses'] | data[3][harga]|data[3][stock] | data [3]['roaster']|)
    
    while True:
        input_konfirmasi_hapus = input('lanjut menghapus data tersebut?(y/n)').lower()
        if input_konfirmasi_hapus == 'y':
        # menggunakan sort, reverse agar dalam proses hapus data, index tidak bergeser, maka perlu dimulai dari index terbesar
            for idx in sorted(index_to_delete, reverse=True):  
                del data[idx]
            print('data berhasil dihapus')
            save_data(data)
            show_item(data)
            index_to_delete.clear()
            return
        elif input_konfirmasi_hapus == 'n':
            index_to_delete.clear()
            return
        else:
            print('input harus y/n')
            continue 
                

def show_keranjang(data):
    jumlah_kerangjang = len(data)
    print('isi keranjang anda:')
    print("-" * 50)
    print(f' origin\t       | jumlah \t| total harga\t|')
    print("-" * 50)
    for i in range(jumlah_kerangjang):
        print(f' {(data[i][0]).ljust(14)}| {str(data[i][1]).ljust(1)} gram \t| {str(data[i][2]).ljust(14)}|')

def transaksi(data):
    # Memeriksa kesediaan data
    if not show_item(data):
        return 
    #list kosong untuk menyimpan item yang dibeli
    list_keranjang = []
    #loop utama proses transaksi
    while True:
        #loop untuk input indeks produk oleh user
        while True:
            try:
                input_user_beli = int(input('masukan index dari origin yang dibeli '))
                if input_user_beli < 0 or input_user_beli >= len(data):
                    print('diluar index!')
                    continue  
                break
            except ValueError:
                print('input harus berupa angka!')
        #loop untuk meminta jumlah barang yang dibeli        
        while True:
            try:
                input_jumlah_beli = int(input('berapa banyak? '))
                #disini memastikan apakah jumlah pembelian melebih stock tersedia
                if input_jumlah_beli > data[input_user_beli]['stock']:
                    print('maaf, jumlah kopi yang dibeli lebih banyak dari stok yang ada.')
                    print(f'jumlah {data[input_user_beli]['origin']} sisa {data[input_user_beli]['stock']}')
                    print("silahkan masukan jumlah dibawah stok")
                    continue
                #memastikan input beli tidak 0 atau negatif
                elif input_jumlah_beli <= 0:
                    print("jumlah pembelian tidak bisa 0 atau negatif")
                    continue    
                break
            except ValueError:
                print('input harus berupa angka!')

        #mengitung total harga per item    
        total_harga_per_item = input_jumlah_beli * data[input_user_beli]['harga']
        
        #menambah item ke list sementara atau list_keranjang
        #pada titik ini list item akan menjad:
        #list_keranjang = [
        # ['origin', jumlah_beli, total_harga_per_item],
        # ]
        list_keranjang.append([data[input_user_beli]['origin'],input_jumlah_beli,total_harga_per_item])
        
        #menguragi stock berdasarkan jumlah yang dibeli
        data[input_user_beli]['stock'] -= input_jumlah_beli
        
        show_keranjang(list_keranjang)
       
       #Loop untuk konfirmasi apakah ada barang lain yang dibeli
        while True:
            input_pembelian_tambahan = input("apakah ada kopi lain yang dibeli?(y/n) ").lower()
            if input_pembelian_tambahan == 'n':
                break
            #jika input 'y' atau 'n' maka akan keluar dari loop konfirmasi
            #lanjut ke kondisional lanjutan 
            elif input_pembelian_tambahan == 'y':
                break
            else:
                print("input harus y/n!")
                continue
        #kondisional lanjutan
        #jika input konfirmasi = 'n' keluar dari loop transaksi
        #jika input konfirmasi = 'y' akan kembali ke awal loop transaksi
        if input_pembelian_tambahan == 'n':
            break
        else:
            continue   
    
    #menghitung total belanja
    total_belanja = 0
    for item in list_keranjang:
        total_belanja += item[2]
    show_keranjang(list_keranjang)
    print(f'\t\t\t  total | {total_belanja}')

    #loop konfirmasi apakah penjualan dilanjut setelah melihat total belanjaan
    while True:
        input_konfirmasi_jual = input("lanjutkan penjualan?(y/n) ").lower()
        if input_konfirmasi_jual == 'y':
            break
        elif input_konfirmasi_jual == 'n':
            #jika input = 'n' atau transaksi dibatalkan,
            #maka stock yang sudah dikurangi perlu dikembalikan ke dictionary data_biji_kopi
            for item in list_keranjang:
                for kopi in data:
                    if kopi['origin'] == item[0]:
                        kopi['stock'] += item[1]
            list_keranjang.clear()
            return
        else:
            print("input harus y/n!")

    #loop proses pembayaran
    while True:
        try:
            nominal_bayar = int(input('berapa nominal yang pelanggan bayarkan?(ketik 0 untuk membatalkan penjualan) '))
            #pembayaran sama dengan total belanja
            if nominal_bayar == total_belanja:
                save_data(data)
                print('ucapkan terima kasih')
                list_keranjang.clear()
                return
            #pembayaran kurang dari total belanja
            elif nominal_bayar < total_belanja and nominal_bayar != 0 :
                selisih_bayar = total_belanja - nominal_bayar
                print(f'transaksi gagal, uangnya kurang {selisih_bayar}')
                continue
            elif nominal_bayar == 0:
                for item in list_keranjang:
                    for kopi in data:
                        if kopi['origin'] == item[0]:
                            kopi['stock'] += item[1]
                list_keranjang.clear()
                print('transaksi dibatalkan')
                print('kembali ke menu awal')
                return  
            else: ##pembayaran lebih dari total belanja,
                #perlu untuk menghitung kembalian
                kembalian = nominal_bayar - total_belanja
                save_data(data)
                print(f"""ucapkan Terima kasih,
                kembaliannya: {kembalian}""")
                list_keranjang.clear()
                return
        except ValueError:
            print('input pembayaran harus berupa angka!')     


main_menu()                     

                                                  