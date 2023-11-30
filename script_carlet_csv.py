import csv
import db

def main():

    make_ids={'BMW':4, 'Audi':2}

    # 開啟 CSV 檔案
    with open('/Users/linyilin/Downloads/hp_data_1.csv', newline='') as csvfile:

        rows = csv.DictReader(csvfile)

        # 以迴圈輸出指定欄位
        for row in rows:


            if row.get('馬力HP') :

                make = row.get('品牌')
                model = row.get('型號')
                trim_level = row.get('車型')
                output = row.get('馬力HP')

                make_id = make_ids.get(make)
                if not make_id:
                    continue

                with db.local_carlet.Session() as session:
                    session.query(db.local_carlet.models.VehicleModel).filter_by(
                        make_id=make_id, 
                        name=model, 
                        trim_level=trim_level
                    ).update({'output': f'{output} hp'})
                    session.commit()
            
                print(f'Make : {make}')
                print(f'Model : {model}')
                print(f'Sub Model : {trim_level}')
                print(f'Output : {output}')




if __name__ == "__main__":

    main()
