import json

import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline as Pipe

from idbadapter.schedule_loader import Schedules, GRANULARY, TYPEDLVL2, PROCESSED
from idbadapter import MschmAdapter
from stairsres.DBWrapper import DBWrapper
from dataset.MSGDataset import MSGDataset
from dataset.WindowDataset import WindowDataset
from dataset.ObjectNameProcessor import ObjectNameProcessor
from bayesian.networks import EgoResourceNet, EgoWorkNet, EgoPerformanceNet
from core.core_utils import gas_ved_dict, new_dormitory_dict
from dataset.PreprocessedMSG import PreprocessedMSG
URL = "postgresql+psycopg2://testuser:pwd@10.32.15.30:25432/test"


# TODO: finish pipeline class
class Pipeline:
    def __init__(self, work_name, work_name_processed, work_vol, project):
        self.work_name = work_name
        self.work_name_processed = work_name_processed
        self.work_vol = work_vol
        self.res_names = None
        # Загружаем ведомость в поле journal
        with open('D:/GPN_KIP/auxiliary_data/journal_mapped.json') as f:
            journal = json.load(f)
        self.journal = journal
        if work_name_processed:
            journal_map = journal[work_name_processed]
            self.res_names = [res_name for res_name in journal_map["resources"]]
            self.adapter = Schedules(URL)
            self.mschm_adapter = MschmAdapter(URL)
            wrapper = DBWrapper(adapter=self.adapter, mschm_adapter=self.mschm_adapter)
            res_mapper = ObjectNameProcessor(wrapper=wrapper)
            res_mapper_dict = res_mapper.create_granulary_dict(self.res_names, name_type='res')
            res_names_processed = []
            change_columns = {work_name_processed: work_name}
            for res_name in res_mapper_dict:
                res_names_processed.append(res_mapper_dict[res_name][0])
                change_columns[res_mapper_dict[res_name][0]] = res_name
            self.res_names_processed = res_names_processed
            self.change_columns = change_columns
            self.meases = [journal_map["measurements"]]
        else:
            print('NO Work in Ved '+work_name)

        # if project == 'electroline':
        #     journal_map = journal[work_name]
        # elif project == 'dormitory':
        #     journal_map = journal[new_dormitory_dict[work_name]]
        # else:
        #     journal_map = journal[gas_ved_dict[work_name]]
        

    def get_subworks(self, res_name):
        works = []
        meases = []
        for work in self.journal:
            if res_name in self.journal[work]["resources"]:
                works.append(work)
                meases.append(self.journal[work]["measurements"])
        return works, meases

    @staticmethod
    def __transform_dict(dict_from_pd: dict) -> dict:
        """
        Transforming res and work names in precalculations from Window Dataset format to usual one
        """
        dict_to_db = {}
        for res_name in dict_from_pd:
            new_res_name = res_name.replace('__res_fact', '')
            dict_to_db[new_res_name] = dict_from_pd[res_name][0]

        return dict_to_db

    def __cut_dataset(self, msg_data):
        """
        Trying to avoid outliers
        """
        q_01, q_09 = msg_data[self.work_name].quantile(q=0.1), msg_data[self.work_name].quantile(q=0.9)
        msg_data = msg_data[q_01 <= msg_data[self.work_name]]
        msg_data = msg_data[msg_data[self.work_name] <= q_09]

        return msg_data

    def __delete_zero_cols(self, msg_data):
        """
        Sometimes you might get the dataset which consists of only zeros
        """
        for col in msg_data.columns:
            if col == self.work_name:
                continue
            else:
                if (msg_data[col] == 0.0).all():
                    del msg_data[col]
        msg_data.loc[len(msg_data)] = 0.0

        return msg_data

    def __rename_cols(self, msg_data):
        """
        Rename columns according to WindowDataset format
        """
        new_cols = {}
        for col in msg_data.columns:
            if col == self.work_name:
                new_col = col + "__act_fact"
            elif col == "date":
                new_col = "Unnamed: 0"
            else:
                new_col = col + "__res_fact"
            new_cols[col] = new_col
        msg_data = msg_data.rename(columns=new_cols)

        return msg_data

    def check_work_name(self, msg_data):
        """
        Sometimes you might get the dataset without work from DataBase
        """
        if self.work_name not in list(msg_data.columns):
            raise Exception(f"NO WORK DATA FOR {self.work_name} IN FIT PERFORMANCE")

    def check_columns(self, msg_data):
        """
        Sometimes you might get the dataset without resources from DataBase
        """
        if len(msg_data.columns) < 2:
            raise Exception(f"NUM OF COLUMNS IS NOT ENOUGH FOR {self.work_name}")

    def __get_node_names_for_bn(self, window_data):
        """
        Defining nodes for EgoWorkNet and EgoPerformanceNet
        """
        new_res_names = []
        for col in window_data.columns:
            if "_prod" in col:
                perf_leaf = col
            elif "_act_fact" in col:
                work_root = col
            elif self.work_name not in col:
                new_res_names.append(col)
        return work_root, perf_leaf, new_res_names

    # def precalculate(self):
    #     work_name, work_name_processed = self.work_name, self.work_name_processed
    #     res_names, main_meases = self.res_names, self.meases
    #     res_names_processed = self.res_names_processed
        #   TODO: after demo uncomment this block
        #
        # subworks_dict = {}
        # for res_name in res_names:
        #     subworks, meases = self.get_subworks(res_name)
        #     subworks_dict[res_name] = {
        #         "measurements": meases,
        #         "subworks": subworks
        #     }
        #
        # first_flag = True
        # third_data = pd.DataFrame()
        # for res_name in res_names:
        #     print(f"GETTING DATA FOR {res_name}")
        #     wrapper = DBWrapper(URL=URL, level=TYPEDLVL2, unit=subworks_dict[res_name]["measurements"])
        #     model = MSGDataset(work_names=subworks_dict[res_name]["subworks"], res_names=[res_name], dbwrapper=wrapper)
        #     data = model.collect()
        #     print("GOT DATA")
        #
        #     bn = EgoResourceNet(root=[work for work in data.columns if work != res_name],
        #                         leaves=[res_name])
        #     nodes = data.columns.tolist()
        #     info = {"types": {
        #         node: "cont" for node in nodes
        #     }, "signs": {
        #         node: "pos" for node in nodes
        #     }}
        #     bn.add_nodes(info)
        #     print("FITTING BAYESIAN NETWORK")
        #     bn.fit(data, silent=True)
        #
        #     path_to_save_bn = '../models/' + bn.name
        #     if not os.path.exists(path_to_save_bn):
        #         os.mkdir(path_to_save_bn)
        #     bn.save(bn_name=path_to_save_bn + '/' + bn.name + '.json', models_dir='./')
        #
        #     data_loader = ResDataset(res_names=[res_name], window_data=data, root_dir="../",
        #                              save_data=False, save_path="./sec.csv")
        #     print("COLLECTING SECONDARY DATA")
        #     second_data = data_loader.collect()
        #     if first_flag:
        #         third_data = pd.concat([third_data, second_data[second_data[work_name] != 0]
        #                                                        [work_name].reset_index(drop=True)], axis=1)
        #         first_flag = False
        #     third_data = pd.concat([third_data, second_data[second_data[work_name] != 0]
        #                                                    [res_name].reset_index(drop=True)], axis=1)

        # wrapper = DBWrapper(adapter=self.adapter, mschm_adapter=self.mschm_adapter, level=GRANULARY, unit=main_meases)
        # model = MSGDataset(work_names=[work_name_processed], res_names=res_names_processed, dbwrapper=wrapper)
        # third_data = model.collect()
        # third_data = third_data.rename(columns=self.change_columns)
        # if work_name not in list(third_data.columns):
        #     print(f"NO WORK DATA FOR {work_name} IN PRECALCULATE")
        #     return None
        # third_data = third_data[third_data[work_name] != 0.0]
        # q_01, q_09 = third_data[work_name].quantile(q=0.1), third_data[work_name].quantile(q=0.9)
        # third_data = third_data[q_01 <= third_data[work_name]]
        # third_data = third_data[third_data[work_name] <= q_09]
        # if len(third_data.columns) < 2:
        #     print('\n\n\n')
        #     print("No resources")
        #     print(work_name, end='\n\n\n')
        #     return None
        # for col in third_data.columns:
        #     if col == work_name:
        #         continue
        #     else:
        #         if (third_data[col] == 0.0).all():
        #             del third_data[col]
        # res_names = [col for col in third_data.columns if col != work_name]
        # third_data.loc[len(third_data)] = 0.0
        #
        # bn_05 = EgoWorkNet(root=[work_name], leaves=res_names)
        # bn_01 = EgoWorkNet(root=[work_name], leaves=res_names, quantile='0.1')
        # bn_09 = EgoWorkNet(root=[work_name], leaves=res_names, quantile='0.9')
        #
        # nodes = third_data.columns.tolist()
        # info = {"types": {
        #     node: "cont" for node in nodes
        # }, "signs": {
        #     node: "pos" for node in nodes
        # }}
        #
        # bn_05.add_nodes(info)
        # bn_01.add_nodes(info)
        # bn_09.add_nodes(info)
        # bn_05.fit(third_data, silent=True)
        # bn_01.fit(third_data, silent=True)
        # bn_09.fit(third_data, silent=True)
        #
        # precalculation = {}
        # min_grid = third_data[work_name].min()
        # max_grid = third_data[work_name].max()
        # n = 30
        # h = (max_grid - min_grid) / n
        # test_value = min_grid
        #
        # for _ in range(n):
        #     test_data = pd.DataFrame({work_name: [test_value]})
        #     res_pred_05 = bn_05.predict(test_data)[res_names].to_dict('list')
        #     res_pred_01 = bn_01.predict(test_data)[res_names].to_dict('list')
        #     res_pred_09 = bn_09.predict(test_data)[res_names].to_dict('list')
        #
        #     res_pred_05 = self.__transform_dict(res_pred_05)
        #     res_pred_01 = self.__transform_dict(res_pred_01)
        #     res_pred_09 = self.__transform_dict(res_pred_09)
        #
        #     precalculation_for_value = {
        #         "10%": res_pred_01,
        #         "50%": res_pred_05,
        #         "90%": res_pred_09,
        #         "Prob": 0.0
        #     }
        #
        #     precalculation[test_value] = precalculation_for_value
        #     test_value += h
        #
        # work_name = work_name.replace('/', '#')
        # with open(f'./precalc_{work_name}.json', 'w') as fp:
        #     json.dump({work_name: precalculation}, fp)
        #
        # # wrapper = DBWrapper(URL=URL)
        # # wrapper.save_precalculation({work_name: precalculation})
        #
        # return precalculation

    def fit_performance(self, ved_mapper):
        if self.res_names:
            work_name, work_name_processed = self.work_name, self.work_name_processed
            res_names, main_meases = self.res_names, self.meases
            res_names_processed = self.res_names_processed
            file = open('D:/GPN_KIP/auxiliary_data/journal_mapped.json')
            journal = json.load(file)
            print([work_name_processed])
            print(res_names_processed)
            # getting MSG Dataset
            wrapper = DBWrapper(adapter=self.adapter, mschm_adapter=self.mschm_adapter, level=GRANULARY, unit=main_meases)
            #model = MSGDataset(work_names=[work_name_processed], res_names=res_names_processed, dbwrapper=wrapper)
            model = PreprocessedMSG(key_work_name=[work_name_processed], res_names=res_names_processed,dbwrapper=wrapper, journal=journal)
            msg_data = model.collect()
            # if len(msg_data) <= 50:
            #     model = MSGDataset(work_names=[work_name_processed], res_names=res_names_processed, dbwrapper=wrapper,
            #                        delete_zero_res=False)
            #     msg_data = model.collect()
            # preprocessing MSG Dataset
            try:
                if msg_data is not None:
                    msg_data = msg_data.rename(columns=self.change_columns)
                    self.check_work_name(msg_data=msg_data)
                    msg_data = msg_data[msg_data[work_name] != 0.0]
                    msg_data = self.__cut_dataset(msg_data=msg_data)
                    self.check_columns(msg_data=msg_data)
                    msg_data = self.__delete_zero_cols(msg_data=msg_data)
                    msg_data = self.__rename_cols(msg_data=msg_data)
                    self.check_columns(msg_data=msg_data)
            except Exception as error:
                print("ERROR: ", error)
                return None
            

            if msg_data is not None and msg_data.shape[0] > 30:
                # getting Window Dataset
                window_data_wrapper = WindowDataset(msg_data=msg_data, min_window=2, max_window=15)
                window_data = window_data_wrapper.collect()

                work_root, perf_leaf, new_res_names = self.__get_node_names_for_bn(window_data=window_data)

                # init regressor for EgoPerformanceNet
                stages = [('polynomial', PolynomialFeatures(degree=3)),
                            ('mode', LinearRegression())]
                pipeline = Pipe(stages)

                bn_05_perf = EgoPerformanceNet(root=new_res_names, leaves=[perf_leaf], regressor=pipeline)
                bn_01_perf = EgoPerformanceNet(root=new_res_names, leaves=[perf_leaf], quantile='0.1', regressor=pipeline)
                bn_09_perf = EgoPerformanceNet(root=new_res_names, leaves=[perf_leaf], quantile='0.9', regressor=pipeline)

                bn_05 = EgoWorkNet(root=[work_root], leaves=new_res_names)
                bn_01 = EgoWorkNet(root=[work_root], leaves=new_res_names, quantile='0.1')
                bn_06 = EgoWorkNet(root=[work_root], leaves=new_res_names, quantile='0.6')
                bn_07 = EgoWorkNet(root=[work_root], leaves=new_res_names, quantile='0.7')
                bn_08 = EgoWorkNet(root=[work_root], leaves=new_res_names, quantile='0.8')
                bn_09 = EgoWorkNet(root=[work_root], leaves=new_res_names, quantile='0.9')

                nodes = new_res_names + [perf_leaf]
                info = {"types": {
                    node: "cont" for node in nodes
                }, "signs": {
                    node: "pos" for node in nodes
                }}

                bn_05_perf.add_nodes(info)
                bn_01_perf.add_nodes(info)
                bn_09_perf.add_nodes(info)
                bn_05_perf.fit(window_data[bn_05_perf.root + bn_05_perf.leaves])
                bn_01_perf.fit(window_data[bn_05_perf.root + bn_05_perf.leaves])
                bn_09_perf.fit(window_data[bn_05_perf.root + bn_05_perf.leaves])

                work_name = work_name.replace('/', '#')
                work_name = work_name.replace('*', '#')
                work_name = work_name.replace('+', '#')
                work_name = work_name.replace('-', '#')
                work_name = work_name.replace('"', '#')
                bn_05_perf.save(bn_name=f'./{work_name}_05')
                bn_09_perf.save(bn_name=f'./{work_name}_09')
                bn_01_perf.save(bn_name=f'./{work_name}_01')

                nodes = new_res_names + [work_root]
                info = {"types": {
                    node: "cont" for node in nodes
                }, "signs": {
                    node: "pos" for node in nodes
                }}

                bn_01.add_nodes(info)
                bn_05.add_nodes(info)
                bn_06.add_nodes(info)
                bn_07.add_nodes(info)
                bn_08.add_nodes(info)
                bn_09.add_nodes(info)

                bn_01.fit(window_data[bn_01.root + bn_01.leaves], silent=True)
                bn_05.fit(window_data[bn_01.root + bn_01.leaves], silent=True)
                bn_06.fit(window_data[bn_01.root + bn_01.leaves], silent=True)
                bn_07.fit(window_data[bn_01.root + bn_01.leaves], silent=True)
                bn_08.fit(window_data[bn_01.root + bn_01.leaves], silent=True)
                bn_09.fit(window_data[bn_01.root + bn_01.leaves], silent=True)

                precalculation = {}
                min_grid = min(window_data[work_root].min(), self.work_vol)
                max_grid = max(window_data[work_root].max(), self.work_vol)
                n = 30
                h = (max_grid - min_grid) / n
                test_value = min_grid

                for _ in range(n):
                    test_data = pd.DataFrame({work_root: [test_value]})
                    res_pred_05 = bn_05.predict(test_data)[new_res_names].to_dict('list')
                    res_pred_01 = bn_01.predict(test_data)[new_res_names].to_dict('list')
                    res_pred_06 = bn_06.predict(test_data)[new_res_names].to_dict('list')
                    res_pred_07 = bn_07.predict(test_data)[new_res_names].to_dict('list')
                    res_pred_08 = bn_08.predict(test_data)[new_res_names].to_dict('list')
                    res_pred_09 = bn_09.predict(test_data)[new_res_names].to_dict('list')

                    res_pred_05 = self.__transform_dict(res_pred_05)
                    res_pred_01 = self.__transform_dict(res_pred_01)
                    res_pred_06 = self.__transform_dict(res_pred_06)
                    res_pred_07 = self.__transform_dict(res_pred_07)
                    res_pred_08 = self.__transform_dict(res_pred_08)
                    res_pred_09 = self.__transform_dict(res_pred_09)

                    precalculation_for_value = {
                        "10%": res_pred_01,
                        "50%": res_pred_05,
                        "60%": res_pred_06,
                        "70%": res_pred_07,
                        "80%": res_pred_08,
                        "90%": res_pred_09,
                        "Prob": 0.0
                    }

                    precalculation[test_value] = precalculation_for_value
                    test_value += h

                work_name = work_name.replace('/', '#')
                with open(f'./precalc_{work_name}.json', 'w') as fp:
                    json.dump({work_name: precalculation}, fp)
            else:
                print('JOURNAL learning')
                work_root = work_name
                perf_leaf = work_name
                new_res_names = res_names

                
                

                # init regressor for EgoPerformanceNet
                stages = [('polynomial', PolynomialFeatures(degree=3)),
                            ('mode', LinearRegression())]
                pipeline = Pipe(stages)

                bn_05_perf = EgoPerformanceNet(root=new_res_names, leaves=[perf_leaf], regressor=pipeline, mapper=ved_mapper)
                bn_01_perf = EgoPerformanceNet(root=new_res_names, leaves=[perf_leaf], quantile='0.1', regressor=pipeline, mapper=ved_mapper)
                bn_09_perf = EgoPerformanceNet(root=new_res_names, leaves=[perf_leaf], quantile='0.9', regressor=pipeline, mapper=ved_mapper)

                bn_05 = EgoWorkNet(root=[work_root], leaves=new_res_names, mapper=ved_mapper)
                bn_01 = EgoWorkNet(root=[work_root], leaves=new_res_names, quantile='0.1', mapper=ved_mapper)
                bn_06 = EgoWorkNet(root=[work_root], leaves=new_res_names, quantile='0.6', mapper=ved_mapper)
                bn_07 = EgoWorkNet(root=[work_root], leaves=new_res_names, quantile='0.7', mapper=ved_mapper)
                bn_08 = EgoWorkNet(root=[work_root], leaves=new_res_names, quantile='0.8',mapper=ved_mapper)
                bn_09 = EgoWorkNet(root=[work_root], leaves=new_res_names, quantile='0.9',mapper=ved_mapper)

                nodes = new_res_names + [perf_leaf]
                info = {"types": {
                    node: "cont" for node in nodes
                }, "signs": {
                    node: "pos" for node in nodes
                }}

                bn_05_perf.add_nodes(info)
                bn_01_perf.add_nodes(info)
                bn_09_perf.add_nodes(info)
                bn_05_perf.fit(data=None)
                bn_01_perf.fit(data=None)
                bn_09_perf.fit(data=None)

                work_name = work_name.replace('/', '#')
                work_name = work_name.replace('*', '#')
                work_name = work_name.replace('+', '#')
                work_name = work_name.replace('-', '#')
                work_name = work_name.replace('"', '#')
                bn_05_perf.save(bn_name=f'./{work_name}_05')
                bn_09_perf.save(bn_name=f'./{work_name}_09')
                bn_01_perf.save(bn_name=f'./{work_name}_01')

                nodes = new_res_names + [work_root]
                info = {"types": {
                    node: "cont" for node in nodes
                }, "signs": {
                    node: "pos" for node in nodes
                }}

                bn_01.add_nodes(info)
                bn_05.add_nodes(info)
                bn_06.add_nodes(info)
                bn_07.add_nodes(info)
                bn_08.add_nodes(info)
                bn_09.add_nodes(info)

                bn_01.fit(data=None)
                bn_05.fit(data=None)
                bn_06.fit(data=None)
                bn_07.fit(data=None)
                bn_08.fit(data=None)
                bn_09.fit(data=None)

                precalculation = {}
                min_grid = self.work_vol
                max_grid = 30*self.work_vol
                n = 30
                h = (max_grid - min_grid) / n
                test_value = min_grid

                for _ in range(n):
                    test_data = pd.DataFrame({work_root: [test_value]})
                    res_pred_05 = bn_05.predict(test_data)[new_res_names].to_dict('list')
                    res_pred_01 = bn_01.predict(test_data)[new_res_names].to_dict('list')
                    res_pred_06 = bn_06.predict(test_data)[new_res_names].to_dict('list')
                    res_pred_07 = bn_07.predict(test_data)[new_res_names].to_dict('list')
                    res_pred_08 = bn_08.predict(test_data)[new_res_names].to_dict('list')
                    res_pred_09 = bn_09.predict(test_data)[new_res_names].to_dict('list')

                    res_pred_05 = self.__transform_dict(res_pred_05)
                    res_pred_01 = self.__transform_dict(res_pred_01)
                    res_pred_06 = self.__transform_dict(res_pred_06)
                    res_pred_07 = self.__transform_dict(res_pred_07)
                    res_pred_08 = self.__transform_dict(res_pred_08)
                    res_pred_09 = self.__transform_dict(res_pred_09)

                    precalculation_for_value = {
                        "10%": res_pred_01,
                        "50%": res_pred_05,
                        "60%": res_pred_06,
                        "70%": res_pred_07,
                        "80%": res_pred_08,
                        "90%": res_pred_09,
                        "Prob": 0.0
                    }

                    precalculation[test_value] = precalculation_for_value
                    test_value += h

                work_name = work_name.replace('/', '#')
                with open(f'./precalc_{work_name}.json', 'w') as fp:
                    json.dump({work_name: precalculation}, fp)

        else:
            print('Problems with ' + self.work_name)
            return None

        # wrapper = DBWrapper(URL=URL)
        # wrapper.save_model({work_name + '_0.5': bn_05.get_params_for_db()})
        # wrapper.save_model({work_name + '_0.1': bn_01.get_params_for_db()})
        # wrapper.save_model({work_name + '_0.9': bn_09.get_params_for_db()})
