import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
from .opt_Bayes import opt_Bayes
import re
import math

def Solver_MultiBiFirst_func(init_dict):
    print('Program will fit the data with multilevel bivariate first-order differential equations.')
    print('The multilevel differential equations are:')
    print('dx/dt = (beta1 + etaI1) * x + (beta2 + etaI2) * y')
    print('dy/dt = (beta3 + etaI3) * x + (beta4 + etaI4) * y')
    print('Optimizing...')

    userdata = init_dict["userdata"]
    modelDF = init_dict["modelDF"]
    field_model = init_dict["field_model"]
    multi_model = init_dict["multi_model"]
    order_model = init_dict["order_model"]
    var_model = init_dict["var_model"]
    guess = init_dict["guess"]
    method = init_dict["method"]
    subject_model = init_dict["subject_model"]
    bayes_obj = init_dict["bayesian_obj"]
    mid_notime_field = var_model.loc[var_model['field'] != 'time', 'field'].values

    space = {'beta1':bayes_obj(-3,3),
                'beta2':bayes_obj(-3,3),
               'beta3':bayes_obj(-3,3),
               'beta4':bayes_obj(-3,3),
               'init_x':bayes_obj(-20,20),
               'init_y':bayes_obj(-20,20),}
    n_seed = 30
    n_total = 2000
    gamma = 0.8
    ############################
    # optimization
    # --------------------------
    if method[0]=="bayesian":
        calc_data = calcBayes_MultiBiFirst_func(userdata,
                                                var_model,
                                                method,
                                                subject_model,
                                                modelDF,
                                                space,
                                                n_seed,
                                                n_total,
                                                gamma,
                                                bayes_obj)
        predict_data = calc_data['predict_data']
        random_effects = calc_data["random_effects"]
        fixed_effects = calc_data['fixed_effects']
        bayesFix_data = fixed_effects[fixed_effects['rmse'] == fixed_effects['rmse'].min()]
        bayesFix_best_data = bayesFix_data.iloc[0, :].values
        beta1 = bayesFix_best_data[0]
        beta2 = bayesFix_best_data[1]
        beta3 = bayesFix_best_data[2]
        beta4 = bayesFix_best_data[3]
        init_x = bayesFix_best_data[4]
        init_y = bayesFix_best_data[5]
    else:
        calc_data = calc_MultiBiFirst_func(userdata, var_model, guess, method, subject_model, modelDF)
        predict_data = calc_data['predict_data']
        random_effects = calc_data["random_effects"]
        beta1 = calc_data['fixed_effects'].x[0]
        beta2 = calc_data['fixed_effects'].x[1]
        beta3 = calc_data['fixed_effects'].x[2]
        beta4 = calc_data['fixed_effects'].x[3]
        init_x = calc_data['fixed_effects'].x[4]
        init_y = calc_data['fixed_effects'].x[5]
    ## equation
    equation1 = f"{mid_notime_field[0]}(1) = {beta1} * {mid_notime_field[0]} + {beta2} * {mid_notime_field[1]} \n"
    equation2 = f"{mid_notime_field[1]}(1) = {beta3} * {mid_notime_field[0]} + {beta4} * {mid_notime_field[0]} \n"
    equation3 = f"Init t0_{mid_notime_field[0]}:{init_x}; Init t0_{mid_notime_field[1]}:{init_y} \n"
    ## table
    table = pd.DataFrame({"parameter":[f"{mid_notime_field[0]}(0) to {mid_notime_field[0]}(1)",
                                       f"{mid_notime_field[1]}(0) to {mid_notime_field[0]}(1)",
                                       f"{mid_notime_field[0]}(0) to {mid_notime_field[1]}(1)",
                                       f"{mid_notime_field[1]}(0) to {mid_notime_field[1]}(1)"],
                          "value":[beta1,
                                   beta2,
                                   beta3,
                                   beta4]})
    res_dict = {"solve_data":calc_data['fixed_effects'],
                "userdata":userdata,
                "predict_data":predict_data,
                "table":table,
                "equation":[equation1,equation2,equation3],
                "random_effects":random_effects}
    return res_dict

def calc_MultiBiFirst_func(userdata,var_model,guess,method,subject_model, modelDF):
    ## identify variables and information

    ## fix effect
    mid_var_t = var_model.loc[var_model['field'] == 'time', 'variable'].values[0]
    mid_notime_field = var_model.loc[var_model['field'] != 'time', 'field'].values
    mid_num_t = userdata[mid_var_t].sort_values(ascending=True).unique().tolist()
    mid_num_t = [x for x in mid_num_t if not math.isnan(x)]
    fix_model = modelDF.loc[modelDF['operator'] == '~','fixRand'].tolist()
    # mid_userdata = userdata.loc[:,var_model.loc[:,'variable'].tolist()]
    # rename_key = {k: v for k, v in zip(var_model.loc[:,'variable'].tolist(), var_model.loc[:,'field'].tolist())}
    # mid_userdata.rename(columns=rename_key,inplace=True)
    # mid_userdata["subject"] = userdata.loc[:,subject_model]
    args= [userdata,mid_var_t,mid_num_t,mid_notime_field]
    calcFix_data = minimize(calcFix_MultiBiFirst_func,
                                    x0=guess[0],
                                    method=method[0],
                                    tol=1e-8,
                                    options={'disp': False},
                                    args=args)
    randEffect_data = pd.DataFrame({"Subject":[],
                               "EtaI_1":[],
                               "EtaI_2":[],
                               "EtaI_3":[],
                               "EtaI_4":[],
                               "EtaI_x":[],
                               "EtaI_y":[]})

    # subject_guess
    # --------------------------
    subject_guess = guess[1]
    if not re.search('1', fix_model[0]):
        subject_guess[4] = False
    if not re.search('1', fix_model[1]):
        subject_guess[5] = False
    if not re.search(mid_notime_field[0], fix_model[0]):
        subject_guess[0] = False
    if not re.search(mid_notime_field[1], fix_model[0]):
        subject_guess[1] = False
    if not re.search(mid_notime_field[0], fix_model[1]):
        subject_guess[2] = False
    if not re.search(mid_notime_field[1], fix_model[1]):
        subject_guess[3] = False

    uni_subject_list = userdata[subject_model].unique().tolist()
    uni_subject_list = [x for x in uni_subject_list if not math.isnan(x)]
    for index,i_subject in enumerate(uni_subject_list):
        print(f'Estimating random effects {i_subject}')
        mid_userdata = userdata.loc[userdata[subject_model] == i_subject]
        sub_args = [mid_userdata, mid_var_t, mid_num_t, mid_notime_field, guess[1], subject_guess, calcFix_data.x]
        mid_calcRandom_data = minimize(calcRand_MultiBiFirst_func,
                                    x0=guess[1],
                                    method=method[1],
                                    tol=1e-8,
                                    options={'disp': False},
                                    args=sub_args)
        new_row = [i_subject] + mid_calcRandom_data.x.tolist()
        new_row_df = pd.DataFrame([new_row],columns=randEffect_data.columns)
        randEffect_data = pd.concat([randEffect_data, new_row_df], ignore_index=True)
    # --------------------------
    ## predict data
    predict_data = pd.DataFrame({"Subject": [],
                                    "time": [],
                                    mid_notime_field[0]+"_hat": [],
                                    mid_notime_field[1]+"_hat": []
                                 })
    times = mid_num_t
    for index,i_subject in enumerate(uni_subject_list):
        randEffect_parms = randEffect_data.loc[randEffect_data['Subject'] == i_subject,:]
        mid_predict_y0 = [calcFix_data.x[4] + randEffect_parms.loc[index,'EtaI_x'],
                          calcFix_data.x[5] + randEffect_parms.loc[index,'EtaI_y']]

        mid_predict_parms = [calcFix_data.x[0] + randEffect_parms.loc[index,'EtaI_1'],
                          calcFix_data.x[1] + randEffect_parms.loc[index,'EtaI_2'],
                          calcFix_data.x[2] + randEffect_parms.loc[index,'EtaI_3'],
                          calcFix_data.x[3] + randEffect_parms.loc[index,'EtaI_4']]
        mid_predict_data = solve_ivp(solve_MultiBiFirst_func,
                                 [0, max(mid_num_t)],
                                 y0=mid_predict_y0,
                                 t_eval=mid_num_t,
                                 args=[mid_predict_parms])
        mid_predictDF_data = pd.DataFrame(np.array(mid_predict_data.y).T)
        mid_predictDF_data.rename(columns={0:mid_notime_field[0]+"_hat",1:mid_notime_field[1]+"_hat"},inplace=True)
        mid_predictDF_data['time'] = np.array(mid_num_t)
        mid_predictDF_data['Subject'] = i_subject
        predict_data = pd.concat([predict_data,mid_predictDF_data],axis=0)
    res_dict = {"fixed_effects":calcFix_data,
                "random_effects":randEffect_data,
                "predict_data":predict_data}
    return res_dict

def calcFix_MultiBiFirst_func(x0, args):
    userdata = args[0]
    mid_var_t = args[1]
    mid_num_t = args[2]
    mid_notime_field = args[3]
    mid_min_data = solve_ivp(solve_MultiBiFirst_func,
                             [0, max(mid_num_t)],
                             y0=x0[4:6],
                             t_eval=mid_num_t,
                             args=[x0[0:4]])
    mid_df_res = pd.DataFrame(np.array(mid_min_data.y).T)
    mid_df_res.rename(columns={0:mid_notime_field[0]+"_hat",1:mid_notime_field[1]+"_hat"},inplace=True)
    mid_df_res['time'] = np.array(mid_min_data.t)

    res_df = pd.merge(userdata,mid_df_res,on="time")
    res_sum = []
    for i in mid_notime_field:
        res_df[i+"_err"] = (res_df[i] - res_df[i+"_hat"]) **2
        res_sum.append(res_df[i+"_err"].sum())
    return np.sum(res_sum)

def calcRand_MultiBiFirst_func(x0, args):
    userdata = args[0]
    mid_num_t = args[2]
    mid_notime_field = args[3]
    subject_guess = args[5]
    false_indices = [index for index, value in enumerate(subject_guess) if value is False]
    for index in false_indices:
        x0[index] = 0

    fixed_parms = args[6]
    mid_y0 = x0[4:6] + fixed_parms[4:6]
    mid_args = [x0[0:4] + fixed_parms[0:4]]
    mid_min_data = solve_ivp(solve_MultiBiFirst_func,
                             [0, max(mid_num_t)],
                             y0=mid_y0,
                             t_eval=mid_num_t,
                             args=mid_args)
    mid_df_res = pd.DataFrame(np.array(mid_min_data.y).T)
    mid_df_res.rename(columns={0: mid_notime_field[0] + "_hat", 1: mid_notime_field[1] + "_hat"}, inplace=True)
    if f'{mid_notime_field[1]}_hat' not in mid_df_res.columns.tolist(): #fix bug
        mid_df_res[f'{mid_notime_field[1]}_hat'] = 0
    mid_df_res['time'] = np.array(mid_min_data.t)

    res_df = pd.merge(userdata, mid_df_res, on="time",how="outer")
    res_df.fillna(0,inplace=True)

    res_sum = []
    for i in mid_notime_field:
        res_df.loc[res_df[i + "_hat"] > 1e+50,i + "_hat"] = 0
        res_df.loc[res_df[i + "_hat"] < -1e+50, i + "_hat"] = 0
        res_df = res_df.replace([np.inf, -np.inf], 0)
        res_df[i + "_err"] = (res_df[i] - res_df[i + "_hat"]) ** 2
        res_sum.append(res_df[i + "_err"].sum())
    return np.sum(res_sum)

def solve_MultiBiFirst_func(t, y0, args):
    mid_args_list = list(args)
    dxdt = mid_args_list[0] * y0[0] + mid_args_list[1] * y0[1]
    dydt = mid_args_list[2] * y0[0] + mid_args_list[3] * y0[1]
    return [dxdt, dydt]

############################
    # Bayesian optimization
    # --------------------------
def calcBayes_MultiBiFirst_func(userdata,var_model,
                                method,
                                subject_model,
                                modelDF,
                                space,
                                n_seed,
                                n_total,
                                gamma,
                                bayes_obj):
    ## fix effect
    mid_var_t = var_model.loc[var_model['field'] == 'time', 'variable'].values[0]
    mid_notime_field = var_model.loc[var_model['field'] != 'time', 'field'].values
    mid_num_t = userdata[mid_var_t].sort_values(ascending=True).unique().tolist()
    fix_model = modelDF.loc[modelDF['operator'] == '~', 'fixRand'].tolist()
    args = {"mid_notime_field":mid_notime_field,
            "subject_model":subject_model}
    calcFix_data = opt_Bayes(userdata,
                             space,
                             n_seed,
                             n_total,
                             gamma,
                             fmin_rmse = fmin_rmse,
                             args=args)
    print('calcFix_data',calcFix_data)
    bayesFix_data = calcFix_data[calcFix_data['rmse'] == calcFix_data['rmse'].min()]
    print('bayesFix_data',bayesFix_data)

    randEffect_data = pd.DataFrame({"Subject": [],
                                    "EtaI_1": [],
                                    "EtaI_2": [],
                                    "EtaI_3": [],
                                    "EtaI_4": [],
                                    "EtaI_x": [],
                                    "EtaI_y": [],
                                    "RMSE": []})

    # subject_guess
    # --------------------------
    fixed = [0,0,0,0,0,0]
    if not re.search('1', fix_model[0]):
        fixed[5] = False
    if not re.search('1', fix_model[1]):
        fixed[6] = False
    if not re.search(mid_notime_field[0], fix_model[0]):
        fixed[0] = False
    if not re.search(mid_notime_field[1], fix_model[0]):
        fixed[1] = False
    if not re.search(mid_notime_field[0], fix_model[1]):
        fixed[2] = False
    if not re.search(mid_notime_field[1], fix_model[1]):
        fixed[3] = False
    args_rand = {"mid_notime_field": mid_notime_field,
                "subject_model": subject_model,
                 "fixed":fixed,
                 "bayesFix_data":bayesFix_data}
    space_rand = {'beta1': bayes_obj(-3, 3),
             'beta2': bayes_obj(-3, 3),
             'beta3': bayes_obj(-3, 3),
             'beta4': bayes_obj(-3, 3),
             'init_x': bayes_obj(-20, 20),
             'init_y': bayes_obj(-20, 20), }
    n_seed_rand = 30
    n_total_rand = 2000
    gamma_rand = 0.8

    for index, i_subject in enumerate(userdata[subject_model].unique().tolist()):
        print(f'Estimating random effects {i_subject}')
        mid_userdata = userdata.loc[userdata[subject_model] == i_subject]
        mid_calcRandom_data = opt_Bayes(mid_userdata,
                                     space_rand,
                                     n_seed_rand,
                                     n_total_rand,
                                     gamma_rand,
                                     fmin_rmse = fmin_rmse_rand,
                                     args=args_rand)
        bayesRand_data = mid_calcRandom_data[mid_calcRandom_data['rmse'] == mid_calcRandom_data['rmse'].min()]
        print(bayesRand_data)
        new_row = [i_subject]
        new_row.extend(bayesRand_data.iloc[0,:].values)
        print(bayesRand_data.iloc[0,:].values)
        new_row_df = pd.DataFrame([new_row], columns=randEffect_data.columns)
        randEffect_data = pd.concat([randEffect_data, new_row_df], ignore_index=True)
        print(f"Estimating Random effects: \n {randEffect_data}")

    # --------------------------
    ## predict data
    predict_data = pd.DataFrame({"Subject": [],
                                 "time": [],
                                 mid_notime_field[0] + "_hat": [],
                                 mid_notime_field[1] + "_hat": []
                                 })
    bayesFix_best_data = bayesFix_data.iloc[0, :].values
    times = mid_num_t
    for index, i_subject in enumerate(userdata[subject_model].unique().tolist()):
        randEffect_parms = randEffect_data.loc[randEffect_data['Subject'] == i_subject, :]
        mid_predict_y0 = [bayesFix_best_data[4] + randEffect_parms.loc[index, 'EtaI_x'],
                          bayesFix_best_data[5] + randEffect_parms.loc[index, 'EtaI_y']]

        mid_predict_parms = [bayesFix_best_data[0] + randEffect_parms.loc[index, 'EtaI_1'],
                             bayesFix_best_data[1] + randEffect_parms.loc[index, 'EtaI_2'],
                             bayesFix_best_data[2] + randEffect_parms.loc[index, 'EtaI_3'],
                             bayesFix_best_data[3] + randEffect_parms.loc[index, 'EtaI_4']]
        mid_predict_data = solve_ivp(solve_MultiBiFirst_func,
                                     [0, max(mid_num_t)],
                                     y0=mid_predict_y0,
                                     t_eval=mid_num_t,
                                     args=[mid_predict_parms])
        mid_predictDF_data = pd.DataFrame(np.array(mid_predict_data.y).T)
        mid_predictDF_data.rename(columns={0: mid_notime_field[0] + "_hat", 1: mid_notime_field[1] + "_hat"},
                                  inplace=True)
        mid_predictDF_data['time'] = np.array(mid_num_t)
        mid_predictDF_data['Subject'] = i_subject
        predict_data = pd.concat([predict_data, mid_predictDF_data], axis=0)
    res_dict = {"fixed_effects": calcFix_data,
                "random_effects": randEffect_data,
                "predict_data": predict_data}
    return res_dict
def fmin_rmse(userdata,parms,args):
    times = userdata.loc[:, 'time'].sort_values(ascending=True).unique().tolist()
    mid_y0 = [parms[4],parms[5]]
    mid_args = [parms[0],parms[1],parms[2],parms[3]]
    mid_min_data = solve_ivp(solve_MultiBiFirst_func,
                          [0, 1000],
                          y0=mid_y0,
                          args=[mid_args],
                          t_eval=times
                          )
    mid_df_res = pd.DataFrame(np.array(mid_min_data.y).T)
    mid_df_res.rename(columns={0: args["mid_notime_field"][0] + "_hat", 1: args["mid_notime_field"][1] + "_hat"}, inplace=True)
    mid_df_res['time'] = np.array(mid_min_data.t)

    res_df = pd.merge(userdata, mid_df_res, on="time",how="outer")
    res_df.fillna(0, inplace=True)
    res_sum = []
    for i in args["mid_notime_field"]:
        res_df.loc[res_df[i + "_hat"] > 1e+50, i + "_hat"] = 0
        res_df.loc[res_df[i + "_hat"] < -1e+50, i + "_hat"] = 0
        res_df = res_df.replace([np.inf, -np.inf], 0)
        res_df[i + "_err"] = (res_df[i] - res_df[i + "_hat"]) ** 2
        res_sum.append(res_df[i + "_err"].sum())
    return np.sum(res_sum)

def fmin_rmse_rand(userdata,parms,args):
    fixed= args["fixed"]
    bayesFix_data = args["bayesFix_data"]
    bayesFix_data = bayesFix_data.iloc[0,:].values

    false_indices = [index for index, value in enumerate(fixed) if value is False]
    for index in false_indices:
        parms[index] = 0
        fixed[index] = 0

    times = userdata.loc[:, 'time'].sort_values(ascending=True).unique().tolist()
    mid_y0 = [parms[4] + bayesFix_data[4],
              parms[5] + bayesFix_data[5]]
    mid_args = [parms[0] + bayesFix_data[0],
                parms[1] + bayesFix_data[1],
                parms[2] + bayesFix_data[2],
                parms[3] + bayesFix_data[3]]
    mid_min_data = solve_ivp(solve_MultiBiFirst_func,
                          [0, 1000],
                          y0=mid_y0,
                          args=[mid_args],
                          t_eval=times
                          )
    mid_df_res = pd.DataFrame(np.array(mid_min_data.y).T)
    mid_df_res.rename(columns={0: args["mid_notime_field"][0] + "_hat", 1: args["mid_notime_field"][1] + "_hat"}, inplace=True)
    mid_df_res['time'] = np.array(mid_min_data.t)

    res_df = pd.merge(userdata, mid_df_res, on="time",how="outer")
    res_df.fillna(0, inplace=True)
    res_sum = []
    for i in args["mid_notime_field"]:
        res_df.loc[res_df[i + "_hat"] > 1e+50, i + "_hat"] = 0
        res_df.loc[res_df[i + "_hat"] < -1e+50, i + "_hat"] = 0
        res_df = res_df.replace([np.inf, -np.inf], 0)
        res_df[i + "_err"] = (res_df[i] - res_df[i + "_hat"]) ** 2
        res_sum.append(res_df[i + "_err"].sum())
    return np.sum(res_sum)