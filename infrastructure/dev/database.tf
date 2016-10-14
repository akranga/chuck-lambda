resource "aws_dynamodb_table" "chuck" {
    name = "${var.apex_environment}_chuck"
    read_capacity = 20
    write_capacity = 20
    hash_key = "JokeNumber"
    range_key = "ChuckNorrisFact"
    attribute {
      name = "JokeNumber"
      type = "N"
    }
    attribute {
      name = "ChuckNorrisFact"
      type = "S"
    }
    # attribute {
    #   name = "TopScore"
    #   type = "N"
    # }
    global_secondary_index {
      name = "ChuckNorrisFactIndex"
      hash_key = "ChuckNorrisFact"
      # range_key = "TopScore"
      write_capacity = 10
      read_capacity = 10
      projection_type = "INCLUDE"
      non_key_attributes = [ "JokeNumber" ]
    }
}