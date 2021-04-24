import json
import csv
import scipy.stats
from scipy.stats import binom_test
import numpy as np
import reformat_data
import statistics as stat
from scipy.stats import norm
import math
Z = norm.ppf


#define directories
processed_dir = './processed'
analyzed_dir = './analyzed'
all_data_path = processed_dir + "/Seq_comp_all_subjects.json"
responses_excluded=0

all_sets = []
no_serious = ['SeqC0009','SeqC0108','SeqC0109','SeqC0111','SeqC0117','SeqC0131','SeqC0138','SeqC0154']
no_understand = ['SeqC0009','SeqC0108','SeqC0109','SeqC0111','SeqC0131','SeqC0147']


def SDT(hits, misses, fas, crs):
        #https://lindeloev.net/calculating-d-in-python-and-php/
        """ returns a dict with d-prime measures given hits, misses, false alarms, and correct rejections"""
        # Floors an ceilings are replaced by half hits and half FA's
        half_hit = 0.5 / (hits + misses)
        half_fa = 0.5 / (fas + crs)

        # Calculate hit_rate and avoid d' infinity
        hit_rate = hits / (hits + misses)
        if hit_rate == 1:
                hit_rate = 1 - half_hit
        if hit_rate == 0:
                hit_rate = half_hit

        # Calculate false alarm rate and avoid d' infinity
        fa_rate = fas / (fas + crs)
        if fa_rate == 1:
                fa_rate = 1 - half_fa
        if fa_rate == 0:
                fa_rate = half_fa

        # Return d', beta, c and Ad'
        out = {}
        out['d'] = Z(hit_rate) - Z(fa_rate)
        out['beta'] = math.exp((Z(fa_rate) ** 2 - Z(hit_rate) ** 2) / 2)
        out['c'] = -(Z(hit_rate) + Z(fa_rate)) / 2
        out['Ad'] = norm.cdf(out['d'] / math.sqrt(2))

        return (out)
def get_json(path):
        json_file = open(path)
        json_file = json_file.read()
        return json.loads(json_file)

def mean(ls):
        if len(ls)>0:
                return stat.mean(ls)
        return float('NaN')

def make_csv(subs, keys_to_store,filename='/seq_results.csv'):
        subs = [sub for sub in subs if 'analyzed' in sub] #only analyze subjects that have data
        with open(analyzed_dir + filename, 'w', newline='') as file:
                writer = csv.writer(file)
                keys = ['Subject_ID','excluded'] + keys_to_store
                writer.writerow(keys)

                for s in subs:
                        values = [s['id'],s['excluded']]
                        for key in keys_to_store:
                                values.append(s['analyzed'][key])

                        writer.writerow(values)
        print("Aggregate analysis file saved.")
        return False

def make_json(subs):
        json_export = json.dumps(subs)
        f = open(analyzed_dir + "/seq_results.json", "w")
        f.write(json_export)
        f.close()
        print("saved data.")

reformat_data.run()

all_subjects = get_json(all_data_path)



for s in all_subjects: #every subject in the cohort
        s['excluded']=False
        if(s['id'] in no_serious): s['excluded']=True
        if (s['id'] in no_understand): s['excluded'] = True
        s['analyzed']={
                'block':[],
        }
        block_ids_to_run = [i for i in range(2,12)] #skipping block 1 which is the practice block
        #you can run specific blocks by uncommenting below
        # block_ids_to_run = [1]

        #This task doesn't have a practice block
        # #don't run the practice block:
        # block_ids_to_run.remove(0) #practice block is index 0

        for block in s['blocks']: #every block for the subject
                if(block['block'] not in block_ids_to_run): continue #if it's not in the blocks we want, skip it
                data = {

                        'trials_total': 0,
                        'trials_diatonic': 0,
                        'trials_chromatic': 0,
                        'confidence':[],
                        'confidence_correct': [],
                        'confidence_diatonic': [],
                        'confidence_chromatic': [],
                        'confidence_diatonic_correct': [],
                        'confidence_chromatic_correct': [],
                        'hits':0,
                        'FAs':0,
                        'misses':0,
                        'CRs':0,
                        'd_hit':0,
                        'd_FA': 0,
                        'd_miss': 0,
                        'd_CR': 0,
                        'c_hit': 0,
                        'c_FA': 0,
                        'c_miss': 0,
                        'c_CR': 0,
                        'rts': [],
                        'pressed_button1':0,
                        'pressed_button2': 0,
                }
                for Q in block['repetition']: #Q is every question/trial in the block
                        Q['excluded'] = False
                        # Trial level Time-based exclusion should be written here

                        if(Q['name']!='choice'): continue #if not a choice question, continue to next Q

                        if(Q['char']=='L'):
                                data['pressed_button1']+=1
                        elif (Q['char'] == 'A'):
                                data['pressed_button2'] += 1
                        else:
                                print("there was an error.")

                        data['trials_total'] += 1
                        if(Q['trial_type']=="diatonic"):
                                data['trials_diatonic']+=1

                        elif (Q['trial_type'] == "chromatic"):
                                data['trials_chromatic'] += 1




                        if (Q['trial_type'] == "diatonic"):
                                if(Q['violated']==False and Q['response']==True): #hit
                                        data['hits']+=1
                                        data['d_hit'] += 1
                                elif (Q['violated'] == False and Q['response'] == False):  # miss
                                        data['misses'] += 1
                                        data['d_miss'] += 1
                                elif (Q['violated'] == True and Q['response'] == True):  # FA
                                        data['FAs'] += 1
                                        data['d_FA'] += 1
                                elif (Q['violated'] == True and Q['response'] == False):  # FA
                                        data['CRs'] += 1
                                        data['d_CR'] += 1
                        if (Q['trial_type'] == "chromatic"):
                                if(Q['violated']==False and Q['response']==True): #hit
                                        data['hits']+=1
                                        data['c_hit'] += 1
                                elif (Q['violated'] == False and Q['response'] == False):  # miss
                                        data['misses'] += 1
                                        data['c_miss'] += 1
                                elif (Q['violated'] == True and Q['response'] == True):  # FA
                                        data['FAs'] += 1
                                        data['c_FA'] += 1
                                elif (Q['violated'] == True and Q['response'] == False):  # FA
                                        data['CRs'] += 1
                                        data['c_CR'] += 1

                for i,Q in enumerate(block['confidence']):
                        data['confidence'].append(Q['response'])
                        if(block['repetition'][i]['trial_type']=="diatonic"):
                                data['confidence_diatonic'].append(Q['response'])
                                if((block['repetition'][i]['violated']==False and block['repetition'][i]['response']==True) or (block['repetition'][i]['violated']==True and block['repetition'][i]['response']==False)):
                                        data['confidence_diatonic_correct'].append(Q['response'])
                                        data['confidence_correct'].append(Q['response'])
                        elif (block['repetition'][i]['trial_type'] == "chromatic"):
                                data['confidence_chromatic'].append(Q['response'])
                                if ((block['repetition'][i]['violated'] == False and block['repetition'][i][
                                        'response'] == True) or (
                                        block['repetition'][i]['violated'] == True and block['repetition'][i][
                                        'response'] == False)):
                                        data['confidence_chromatic_correct'].append(Q['response'])
                                        data['confidence_correct'].append(Q['response'])



                s['analyzed']['block'].append(data)

                #once all the per block data was collected(above), append it to subject totales:
                #if the key doesn't exist in the subject level, create it, otherwise, add to it
                for key in data:
                        if (key =="sets"): continue  # don't do it for sets. Sets are handled below
                        try:
                                s['analyzed'][key] += data[key]
                        except:
                                s['analyzed'][key] = data[key]



        sdt_all = SDT(s['analyzed']['hits'],s['analyzed']['misses'],s['analyzed']['FAs'],s['analyzed']['CRs'])
        s['analyzed']['d-prime'] = sdt_all['d']
        s['analyzed']['beta'] = sdt_all['beta']
        s['analyzed']['c'] = sdt_all['c']
        s['analyzed']['Ad'] = sdt_all['Ad']
        s['analyzed']['confidence'] = mean(s['analyzed']['confidence'])
        s['analyzed']['confidence_correct'] = mean(s['analyzed']['confidence_correct'])

        sdt_diatonic = SDT(
                s['analyzed']['d_hit'], s['analyzed']['d_miss'], s['analyzed']['d_FA'], s['analyzed']['d_CR'])
        s['analyzed']['diatonic_d-prime'] = sdt_diatonic['d']
        s['analyzed']['diatonic_beta'] = sdt_diatonic['beta']
        s['analyzed']['diatonic_c'] = sdt_diatonic['c']
        s['analyzed']['diatonic_Ad'] = sdt_diatonic['Ad']
        s['analyzed']['diatonic_confidence'] = mean(s['analyzed']['confidence_diatonic'])
        s['analyzed']['diatonic_conf_to_mean'] = s['analyzed']['diatonic_confidence'] /  s['analyzed']['confidence']
        s['analyzed']['diatonic_correct_confidence'] = mean(s['analyzed']['confidence_diatonic_correct'])
        s['analyzed']['diatonic_correct_conf_to_mean'] = s['analyzed']['diatonic_correct_confidence'] / s['analyzed']['confidence_correct']
        sdt_chromatic = SDT(
                s['analyzed']['c_hit'], s['analyzed']['c_miss'], s['analyzed']['c_FA'], s['analyzed']['c_CR'])
        s['analyzed']['chromatic_d-prime'] = sdt_chromatic['d']
        s['analyzed']['chromatic_beta'] = sdt_chromatic['beta']
        s['analyzed']['chromatic_c'] = sdt_chromatic['c']
        s['analyzed']['chromatic_Ad'] = sdt_chromatic['Ad']
        s['analyzed']['chromatic_confidence'] = mean(s['analyzed']['confidence_chromatic'])
        s['analyzed']['chromatic_conf_to_mean'] = s['analyzed']['chromatic_confidence'] / s['analyzed']['confidence']
        s['analyzed']['chromatic_correct_confidence'] = mean(s['analyzed']['confidence_chromatic_correct'])
        s['analyzed']['chromatic_correct_conf_to_mean'] = s['analyzed']['chromatic_correct_confidence'] / s['analyzed'][
                'confidence_correct']

        s['analyzed']['conf_d:c'] = s['analyzed']['diatonic_confidence'] / s['analyzed']['chromatic_confidence']
        s['analyzed']['conf_correct_d:c'] = s['analyzed']['diatonic_correct_confidence'] / s['analyzed']['chromatic_correct_confidence']

        s['analyzed']['binom'] = binom_test(s['analyzed']['hits']+s['analyzed']['CRs'],s['analyzed']['trials_total'],0.5)


        if(s['analyzed']['binom']>=0.05): s['excluded']=True












keys_to_store = ['trials_total','trials_diatonic','trials_chromatic','d-prime','beta','c','Ad','diatonic_d-prime','diatonic_beta','diatonic_c','diatonic_Ad','diatonic_confidence','diatonic_conf_to_mean','diatonic_correct_confidence','diatonic_correct_conf_to_mean','chromatic_d-prime','chromatic_beta','chromatic_c','chromatic_Ad','chromatic_confidence','chromatic_conf_to_mean','chromatic_correct_confidence','chromatic_correct_conf_to_mean','conf_d:c','conf_correct_d:c','binom']



make_csv(all_subjects, keys_to_store)

make_json(all_subjects)



