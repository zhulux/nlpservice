#!/bin/ruby

require 'csv'

if ARGV.length != 3
  puts "This script extends dataset by replacing entity names"
  puts
  puts "Usage: $0 <amplify_ratio> <mode> <base_corpus>"
  puts
  puts "\tamplify_ratio: A num > 0.0 to specify the num of new records to generate"
  puts "\tmode: (even/freq) even: entity names in generated records will appear evenly; freq: entity names in generated records will appear according to their freq in base dataset"
  puts "\tbase_corpus: the base dataset with headers. It should has 4 cols: new_title, entity, begin, length."
  exit
end


amp_ratio = ARGV[0].to_f
mode = ARGV[1].intern
base_corpus = ARGV[2]

corpus = CSV.read(base_corpus)

headers = corpus[0]
corpus = corpus[1..-1]

entities = corpus.map {|x| x[1] }.uniq


def gen_record(corpus, mode, entities)
  entity = case mode
           when :even then entities.sample
           when :freq then corpus.sample[1]
           end
  record = corpus.sample
  title, orig_entity = record[0].clone, record[1].clone
  begin
    title[orig_entity] = entity
  rescue
    $stderr.puts "Invalid: #{title} [#{orig_entity}]"
    abort
  end
  [title, entity, title.index(entity), entity.length]
end

(amp_ratio * corpus.length).to_i.times.each do
  puts gen_record(corpus, mode, entities).to_csv
end

